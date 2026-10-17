import json, logging, os, re
from contextlib import asynccontextmanager
from pathlib import Path
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, field_validator

MODEL_DIR = Path(os.getenv("SMSGUARD_MODEL_DIR", Path(__file__).resolve().parents[2] / "ml" / "models"))
ORIGINS = os.getenv("SMSGUARD_CORS_ORIGINS", "http://localhost:3000").split(",")
MAX_LEN = 1000
log = logging.getLogger("smsguard")
STATE: dict = {"model": None, "info": None, "metrics": None}

@asynccontextmanager
async def lifespan(app):
    try:
        STATE["model"] = joblib.load(MODEL_DIR / "smsguard_pipeline.joblib")
        STATE["info"] = json.loads((MODEL_DIR / "model_info.json").read_text())
        STATE["metrics"] = json.loads((MODEL_DIR / "metrics.json").read_text())
    except Exception as e:  # never leak paths to clients
        log.error("model load failed: %s", type(e).__name__)
        STATE.update(model=None, info=None, metrics=None)
    yield

app = FastAPI(title="SMSGuard API", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=ORIGINS, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])

class PredictRequest(BaseModel):
    message: str
    @field_validator("message")
    @classmethod
    def check(cls, v):
        v = v.strip()
        if not v: raise ValueError("Message must not be empty.")
        if len(v) > MAX_LEN: raise ValueError(f"Message must be at most {MAX_LEN} characters.")
        return v

class Indicator(BaseModel):
    type: str; detail: str

class PredictResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    label: str; display_label: str; scam_score: float; score_note: str
    indicators: list[Indicator]; guidance: list[str]; model_version: str; disclaimer: str

URGENT = r"\b(urgent(ly)?|immediately|today|now|within \d+ ?(hrs?|hours?|mins?)|blocked|suspended|expire[sd]?|last chance)\b"
SECRET = r"\b(otp|pin|cvv|password|aadhaar|pan|verification code|6 digit code)\b"
MONEY = r"(rs\.?|inr|₹)\s?[\d,]+|\b(fee|processing|deposit|charges?|pay)\b"

def indicators(t: str):
    out, low = [], t.lower()
    if re.search(r"https?://\S+|www\.\S+", low): out.append(Indicator(type="link", detail="Contains a link. Do not open links from unknown senders."))
    if re.search(URGENT, low): out.append(Indicator(type="urgency", detail="Uses urgent or threatening wording to pressure you."))
    if re.search(SECRET, low): out.append(Indicator(type="sensitive_info", detail="Mentions a PIN, OTP, ID or password. Genuine senders never ask you to share these."))
    if re.search(MONEY, low): out.append(Indicator(type="money", detail="Mentions payment, fees or amounts."))
    return out  # simple keyword heuristics, shown as hints, not used for the prediction

GUIDE_SCAM = ["Do not click links or call numbers in the message.", "Never share OTPs, PINs or passwords.",
  "Verify using the official app or the number printed on your card or bill.", "Report suspected fraud at cybercrime.gov.in or call 1930."]
GUIDE_OK = ["No scam pattern was detected, but this is not a guarantee of safety.", "Still avoid sharing OTPs or PINs and verify unexpected requests through official channels."]
DISCLAIMER = "Decision-support prototype trained on synthetic data. A prediction is not proof of fraud or safety."

def ready():
    if STATE["model"] is None: raise HTTPException(503, "Model not available. Run the training pipeline (see docs).")

@app.get("/health")
def health():
    return {"status": "ok", "model_ready": STATE["model"] is not None, "model_version": (STATE["info"] or {}).get("model_version")}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    ready()
    m = STATE["model"]
    p = float(m.predict_proba([req.message])[0][1])
    scam = p >= 0.5
    return PredictResponse(label="scam" if scam else "legitimate", display_label="Potential Scam" if scam else "No Scam Detected",
        scam_score=round(p, 4), score_note="Model score, not a calibrated probability of fraud.",
        indicators=indicators(req.message), guidance=GUIDE_SCAM if scam else GUIDE_OK,
        model_version=STATE["info"]["model_version"], disclaimer=DISCLAIMER)

@app.get("/model-info")
def model_info():
    ready(); return STATE["info"]

@app.get("/metrics")
def metrics():
    ready(); return STATE["metrics"]

@app.get("/dataset-stats")
def dataset_stats():
    f = MODEL_DIR.parent / "reports" / "dataset_report.json"
    if not f.exists(): raise HTTPException(503, "Dataset report not available. Run ml/scripts/validate_dataset.py.")
    return json.loads(f.read_text())

@app.get("/")
def root():
    return {"service": "SMSGuard API", "docs": "/docs", "health": "/health"}
