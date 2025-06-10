from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .models.model_loader import get_model_reports, get_model_metrics
from Backend.models_db import ModelMetrics
from Backend.database import SessionLocal
import pandas as pd
import os
from pydantic import BaseModel
# Initialize FastAPI app
app = FastAPI()

# Allow all CORS (for Streamlit frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory paths
REPORT_DIR = "reports"
METRICS_PATH = "data/model_metrics.csv"

# Dependency: Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "API is live!"}

# Get list of available models
@app.get("/api/models")
def get_models():
    reports = get_model_reports()
    return {"models": list(reports.keys())}

# Get metrics from CSV
@app.get("/api/metrics")
def get_metrics(db: Session = Depends(get_db)):
    try:
        metrics = db.query(ModelMetrics).all()
        if not metrics:
            raise HTTPException(status_code=404, detail="No metrics found in the database.")
        return metrics
    except Exception as e:
        print(f"🔥 ERROR in /metrics: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Get classification report for a specific model
@app.get("/api/reports/{model_name}")
def get_report(model_name: str):
    file_path = os.path.join(REPORT_DIR, f"{model_name}_report.csv")

    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": "Report not found"})

    try:
        df = pd.read_csv(file_path)
        return {"report": df.to_dict(orient="records")}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Store model metrics into PostgreSQL
class MetricInput(BaseModel):
    Model: str
    Accuracy: float
    Precision: float
    Recall: float
    F1_Score: float

@app.post("/api/store-metrics")
def store_metrics(metrics: MetricInput, db: Session = Depends(get_db)):
    model_name = metrics.Model
    existing = db.query(ModelMetrics).filter(ModelMetrics.model_name == model_name).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Model already exists")

    record = ModelMetrics(
        model_name=model_name,
        accuracy=metrics.Accuracy,
        precision=metrics.Precision,
        recall=metrics.Recall,
        f1_score=metrics.F1_Score,
    )
    db.add(record)
    db.commit()
    return {"status": "success"}
# Fetch all metrics from PostgreSQL
@app.get("/api/db-metrics")
def get_all_metrics(db: Session = Depends(get_db)):
    metrics = db.query(ModelMetrics).all()
    return [
        {
            "Model": m.model_name,
            "Accuracy": m.accuracy,
            "Precision": m.precision,
            "Recall": m.recall,
            "F1-Score": m.f1_score
        }
        for m in metrics
    ]
