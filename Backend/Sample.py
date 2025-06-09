import requests

url = "http://localhost:8000/api/store-metrics"

sample_metrics = {
    "Model": "RandomForest",
    "Accuracy": 0.92,
    "Precision": 0.90,
    "Recall": 0.88,
    "F1-Score": 0.89
}

response = requests.post(url, json=sample_metrics)

print("Status:", response.status_code)
print("Response:", response.json())
