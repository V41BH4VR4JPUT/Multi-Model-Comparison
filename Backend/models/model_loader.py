import pandas as pd
import os

REPORT_DIR = os.path.join(os.path.dirname(__file__), "../reports")
METRICS_PATH = os.path.join(os.path.dirname(__file__), "../data/model_metrics.csv")

def get_model_reports():
    reports = {}
    for filename in os.listdir(REPORT_DIR):
        if filename.endswith("_report.csv"):
            model_name = filename.replace("_report.csv", "").replace("_", " ").title()
            df = pd.read_csv(os.path.join(REPORT_DIR, filename))
            reports[model_name] = df.to_dict(orient="records")
    return reports

def get_model_metrics():
    df = pd.read_csv(METRICS_PATH)
    return df.to_dict(orient="records")
