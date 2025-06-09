import optuna
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from joblib import dump
import os

# Load dataset
df = pd.read_csv("data/Wine_Quality_Combined.csv")
X = df.drop(["quality_label", "label", "quality", "wine_type"], axis=1)
y = df["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create output directory
os.makedirs("models/tuned_models", exist_ok=True)

# Define model tuning logic
def tune_model(model_name):
    def objective(trial):
        if model_name == "Random Forest":
            clf = RandomForestClassifier(
                n_estimators=trial.suggest_int("n_estimators", 50, 300),
                max_depth=trial.suggest_int("max_depth", 2, 32),
                min_samples_split=trial.suggest_int("min_samples_split", 2, 10),
                min_samples_leaf=trial.suggest_int("min_samples_leaf", 1, 10),
                random_state=42
            )
        elif model_name == "Logistic Regression":
            clf = LogisticRegression(
                C=trial.suggest_loguniform("C", 1e-4, 1e2),
                solver='liblinear',
                random_state=42
            )
        elif model_name == "Decision Tree":
            clf = DecisionTreeClassifier(
                max_depth=trial.suggest_int("max_depth", 2, 32),
                min_samples_split=trial.suggest_int("min_samples_split", 2, 10),
                min_samples_leaf=trial.suggest_int("min_samples_leaf", 1, 10),
                random_state=42
            )
        elif model_name == "SVM":
            clf = SVC(
                C=trial.suggest_loguniform("C", 1e-3, 1e2),
                gamma=trial.suggest_loguniform("gamma", 1e-4, 1e-1),
                kernel="rbf",
                probability=True,
                random_state=42
            )
        elif model_name == "XGBoost":
            clf = XGBClassifier(
                n_estimators=trial.suggest_int("n_estimators", 50, 300),
                max_depth=trial.suggest_int("max_depth", 2, 32),
                learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3),
                subsample=trial.suggest_float("subsample", 0.5, 1.0),
                colsample_bytree=trial.suggest_float("colsample_bytree", 0.5, 1.0),
                use_label_encoder=False,
                eval_metric='mlogloss',
                random_state=42
            )
        else:
            raise ValueError("Unknown model")

        return cross_val_score(clf, X_train, y_train, cv=5, scoring='accuracy').mean()

    print(f"🔍 Tuning {model_name}...")
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=50)
    print(f"✅ Best Params for {model_name}: {study.best_params}")

    # Train final model on full training data
    best_params = study.best_params
    if model_name == "Random Forest":
        final_model = RandomForestClassifier(**best_params, random_state=42)
    elif model_name == "Logistic Regression":
        final_model = LogisticRegression(**best_params, solver='liblinear', random_state=42)
    elif model_name == "Decision Tree":
        final_model = DecisionTreeClassifier(**best_params, random_state=42)
    elif model_name == "SVM":
        final_model = SVC(**best_params, probability=True, random_state=42)
    elif model_name == "XGBoost":
        final_model = XGBClassifier(**best_params, use_label_encoder=False, eval_metric='mlogloss', random_state=42)

    final_model.fit(X_train, y_train)
    dump(final_model, f"models/tuned_models/{model_name.replace(' ', '_')}.joblib")
    print(f"💾 Saved: models/tuned_models/{model_name.replace(' ', '_')}.joblib\n")

# List of models to tune
models_to_tune = ["Logistic Regression", "Decision Tree", "Random Forest", "SVM", "XGBoost"]

for model in models_to_tune:
    tune_model(model)
