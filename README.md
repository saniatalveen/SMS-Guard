# SMSGuard
English SMS scam detector: FastAPI + scikit-learn backend (web/ Next.js and mobile/ Flutter come next).

## Run
    pip install -r backend/requirements.txt
    python ml/scripts/generate_dataset.py     # seed 42 -> ml/data/sms_dataset.csv
    python ml/scripts/validate_dataset.py     # -> ml/reports/dataset_report.json
    python ml/scripts/train.py                # -> ml/models/{smsguard_pipeline.joblib,model_info.json,metrics.json}
    uvicorn backend.app.main:app --reload     # run from repo root
    cd backend && pytest

Env: SMSGUARD_CORS_ORIGINS (default http://localhost:3000), SMSGUARD_MODEL_DIR.

## Endpoints
GET /health, POST /predict {"message": "..."}, GET /model-info, GET /metrics

## Limits (read before demoing)
- Dataset is 100% synthetic (fictional entities). Metrics are on held-out template families of synthetic data and do NOT show real-world accuracy.
- UCI SMS Spam Collection was not downloaded (no network in build environment). Add it to ml/data and extend train.py to include it.
- Messages are not stored or logged. Indicators (link, urgency, sensitive info, money) are keyword hints, not model output.
