#!/bin/bash

# Start FastAPI backend
if [ "$1" = "backend" ]; then
    uvicorn Backend.main:app --host 0.0.0.0 --port 8000 --reload

# Start Streamlit frontend
elif [ "$1" = "frontend" ]; then
    streamlit run Frontend/Home.py --server.port 8501 --server.address 0.0.0.0

else
    echo "Invalid argument: use 'backend' or 'frontend'"
fi
