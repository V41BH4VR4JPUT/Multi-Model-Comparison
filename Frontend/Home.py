import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Multi-Model Dashboard", layout="wide")

# Greeting
hour = datetime.datetime.now().hour
greeting = (
    "Good Morning ☀️" if hour < 12 else
    "Good Afternoon 🌤️" if hour < 18 else
    "Good Evening 🌙"
)

st.title(f"{greeting} | Welcome to the Multi-Model Comparison Dashboard")

# Banner
st.image("ML Models.png", use_container_width=True)

# Project Overview
st.subheader("📌 Project Overview")
st.markdown("""
This project evaluates multiple machine learning classification models on the Wine Quality dataset. 
The models are compared based on accuracy, precision, recall, and F1-score.
""")

# Steps to Explore
st.subheader("🚀 How to Explore")
st.markdown("""
1. Go to the **Model Details** section to explore each model’s evaluation.
2. Navigate to the **Conclusion** section for final comparison and summary.
3. Use this dashboard to gain insights for final model selection.
""")

# Dataset Info
st.subheader("📚 Dataset Description")
st.markdown("""
- **Source**: [UCI Wine Quality Dataset](https://archive.ics.uci.edu/dataset/186/wine+quality)
- **Features**: 11 chemical attributes like acidity, sugar, pH, alcohol, etc.
- **Target**: Quality score (0–10), grouped into categories (Low, Medium, High)
""")
