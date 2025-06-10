# Multi-Model Comparison & Visualization Dashboard

> A full-stack Machine Learning project to train, evaluate, compare, and visualize multiple classification models using an interactive dashboard built with Streamlit. Backend powered by FastAPI, PostgreSQL for metrics storage, and Docker for seamless containerized deployment.

---

## 🔖 Project Overview

In machine learning development, it's crucial to evaluate multiple models to identify the best fit for your data. This project solves that by:

* Training multiple classification models
* Hyperparameter tuning with Optuna
* Comparing performance metrics
* Storing results in PostgreSQL
* Visualizing comparisons using an interactive Streamlit dashboard

---

## 📊 Datasets

Place your raw and processed data in the `data/` directory.

**Dataset Used**: (You can replace or update this based on the real dataset)

* `data/raw_data.csv`: Original data used for training and testing
* `data/processed_data.csv`: Cleaned and preprocessed version

---

## 🔧 Tech Stack

| Layer          | Tools                                 |
| -------------- | ------------------------------------- |
| 🌎 Frontend    | `Streamlit`, `Matplotlib`, `Seaborn`  |
| 🪄 Backend     | `FastAPI`, `Pydantic`, `Uvicorn`      |
| 🏛️ Database   | `PostgreSQL`, `SQLAlchemy`, `Alembic` |
| 📁 ML/Modeling | `Scikit-learn`, `Optuna`, `joblib`    |
| 🚀 DevOps      | `Docker`, `Docker Compose`            |

---

## 👀 Project Structure

```
Multi-Model-Comparison/
├── Backend/
│   ├── main.py               # FastAPI entrypoint
│   ├── db.py                 # DB connection setup
│   ├── models/
│   │   ├── db_model.py       # SQLAlchemy DB schema
│   │   └── model_loader.py  # Load metrics & reports
│   ├── routers/
│   │   └── api.py            # API route handlers
│   └── .env                  # DB credentials
│
├── frontend/
│   └── app.py                # Streamlit dashboard logic
│
├── notebook/
│   └── model_eval.ipynb      # EDA & evaluation notebook
│
├── reports/
│   └── *.csv                 # Classification reports
│
├── saved_models/            # .joblib or .pkl model files
├── models/
│   └── tuned_models/         # Tuned model dumps
├── optuna_tuner.py          # Hyperparameter tuning script
├── train_models.py          # Base model training script
├── Dockerfile               # For building backend container
├── docker-compose.yml       # For orchestration
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 🌐 Frontend (Streamlit Dashboard)

* Built using `Streamlit`
* Visualizes performance metrics from stored reports and DB
* Supports interactive exploration of accuracy, precision, recall, F1-score

**Pages Include:**

* Model Overview
* Visualized Comparisons
* Raw Metric Table
* Upload new metrics (Optional)

### 📸 Image Slots:

* `Home.png` → Home Page 
* `Model_details.png` → Metrics 
* `Conclusion.png` → Conclusion

---

## 🪄 Backend (FastAPI)

* `/api/store-metrics`: POST API to store model metrics
* `/api/get-metrics`: GET all stored models and metrics
* `/api/get-report/{model_name}`: Get CSV report of specific model

### Key Files:

* `main.py`: Launches FastAPI app
* `db.py`: Initializes DB session
* `db_model.py`: Defines PostgreSQL table `ModelMetrics`
* `model_loader.py`: Functions to load metrics from CSV

---

## 🏛️ PostgreSQL Database

* Stores each model's evaluation metrics
* Table: `ModelMetrics`

**Columns:**

* `id`: Primary key
* `model_name`: Name of the classifier
* `accuracy`, `precision`, `recall`, `f1_score`
* Timestamp (optional)

Connection handled using `SQLAlchemy ORM`.
Environment variables like DB URL, USER, and PASSWORD loaded from `.env`.

---

## 🚀 Dockerization & Deployment

### Dockerfile

```Dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.9'
services:
  backend:
    build: ./Backend
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - ./Backend/.env

  db:
    image: postgres
    environment:
      POSTGRES_USER: youruser
      POSTGRES_PASSWORD: yourpass
      POSTGRES_DB: modelmetrics
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

### .env file

```env
DB_USER=youruser
DB_PASSWORD=yourpass
DB_HOST=db
DB_PORT=5432
DB_NAME=modelmetrics
```

---

## 🔄 Project Phases

### Phase 1: Data Preparation & EDA

* Load and clean dataset
* Visualize correlations & imbalance

### Phase 2: Train Base Models

* Train models: Logistic Regression, SVM, RandomForest, etc.
* Store metrics & reports

### Phase 3: Hyperparameter Tuning (Optuna)

* Use Optuna to tune selected models
* Save top performing models

### Phase 4: Dashboard Integration (Streamlit)

* Connect with reports & PostgreSQL
* Add charts and filters

### Phase 5: Backend API (FastAPI)

* Develop APIs to interact with frontend
* Add validation and error handling

### Phase 6: PostgreSQL Integration

* Setup DB schema with SQLAlchemy
* Store and retrieve metrics dynamically

### Phase 7: Dockerize & Deploy

* Build images
* Use Docker Compose for orchestration
* Optional: Deploy on Render/EC2/VPS

---

## 🚩 Future Improvements

* Add model explainability (SHAP/ELI5)
* Upload new datasets/models from dashboard
* User login and metric filtering
* Deploy on cloud (AWS/GCP/Render)

---

## ✨ Conclusion

This project gives you an end-to-end scalable framework for:

* Evaluating multiple classification models
* Hyperparameter tuning with Optuna
* Storing metrics to a centralized DB
* Creating dashboards for interactive visualization

Ideal for ML engineers, data scientists, or hackathon participants who need quick, robust model comparison pipelines.

---

## 📅 Maintainer

**Vaibhav Rajput**
*AI/ML Developer | Final Year CSE | Open to collaboration*

Feel free to contribute or raise issues!
