import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000/api"

st.title("📊 Model Details")

# 🔹 Step 1: Fetch model list from backend
try:
    response = requests.get(f"{API_URL}/models")
    response.raise_for_status()
    model_list = response.json().get("models", [])
except Exception as e:
    st.error(f"❌ Error fetching model list: {e}")
    model_list = []

# 🔹 Step 2: Show model selection dropdown
if model_list:
    selected_model = st.selectbox("Select a model:", model_list)

    # 🔹 Step 3: Fetch report for selected model
    if selected_model:
        try:
            report_url = f"{API_URL}/reports/{selected_model.replace(' ', '_')}"
            report_response = requests.get(report_url)
            report_response.raise_for_status()
            report_json = report_response.json()

            # ✅ Ensure the key 'report' exists and is list-like
            if "report" in report_json:
                df = pd.DataFrame(report_json["report"])

                st.subheader(f"📄 Classification Report - {selected_model}")
                # Format only numeric columns
                numeric_cols = df.select_dtypes(include='number').columns
                st.dataframe(df.style.format({col: "{:.3f}" for col in numeric_cols}))
            else:
                st.warning("No 'report' data found in response.")

        except Exception as e:
            st.error(f"❌ Error fetching report: {e}")
else:
    st.warning("⚠️ No models found. Please check the backend.")
