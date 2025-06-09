import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from joblib import dump
import os

# Load preprocessed dataset
df = pd.read_csv("Data/Wine_Quality_Combined.csv")

# Prepare features and labels
X = df.drop(columns=["quality", "quality_label", "wine_type", "label"])
y = df["label"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Define models
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss'),
    "SVM": SVC(probability=True)
}

# Create folders to store
os.makedirs("saved_models", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# DataFrame to store all metrics
metrics_list = []

for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

    # Save classification report
    report = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    report_df.to_csv(f"reports/{name.replace(' ', '_')}_report.csv", index=True)

    # Save model
    dump(model, f"saved_models/{name.replace(' ', '_')}.joblib")

    # Save to metrics list
    metrics_list.append({
        "Model": name,
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1-Score": f1
    })

# Save all metrics to CSV
metrics_df = pd.DataFrame(metrics_list)
metrics_df.to_csv("reports/model_metrics.csv", index=False)
print("\n All models trained and saved successfully!")
