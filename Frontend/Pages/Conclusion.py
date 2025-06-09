import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000/api/db-metrics"  # FastAPI endpoint

def fetch_metrics():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error(f"Error fetching data: {response.status_code}")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return pd.DataFrame()

def main():
    st.title("📊 Model Performance Conclusion")
    st.markdown("---")

    metrics_df = fetch_metrics()

    if not metrics_df.empty:
        st.subheader("📈 Stored Model Metrics (From Database)")
        st.dataframe(metrics_df)

        st.subheader("📉 Comparison Charts")
        st.bar_chart(metrics_df.set_index("Model")[["Accuracy", "Precision", "Recall", "F1-Score"]])
    else:
        st.warning("No metrics found in the database.")

if __name__ == "__main__":
    main()
