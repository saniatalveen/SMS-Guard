import sys, importlib
from pathlib import Path
from fastapi.testclient import TestClient
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
def client(monkeypatch=None, model_dir=None):
    import app.main as m
    if model_dir: m.MODEL_DIR = Path(model_dir)
    return TestClient(m.app)
def test_health_and_predict():
    with client() as c:
        assert c.get("/health").json()["model_ready"] is True
        r = c.post("/predict", json={"message": "Your Northstar Bank account will be blocked today. Update KYC at http://example.com/verify"})
        assert r.status_code == 200 and r.json()["label"] == "scam" and r.json()["indicators"]
        r = c.post("/predict", json={"message": "Hey, running 10 mins late. Start without me."})
        assert r.json()["label"] == "legitimate"
def test_validation():
    with client() as c:
        assert c.post("/predict", json={"message": "   "}).status_code == 422
        assert c.post("/predict", json={"message": "a" * 1001}).status_code == 422
        assert c.post("/predict", json={}).status_code == 422
def test_info_metrics():
    with client() as c:
        assert c.get("/model-info").json()["language"] == "en"
        assert "caveat" in c.get("/metrics").json()
def test_missing_model(tmp_path):
    with client(model_dir=tmp_path) as c:
        assert c.get("/health").json()["model_ready"] is False
        r = c.post("/predict", json={"message": "hello"})
        assert r.status_code == 503 and str(tmp_path) not in r.text
