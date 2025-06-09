import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_HOST = os.getenv("DB_HOST", "localhost")  # Default to localhost if not set
DB_PORT = os.getenv("DB_PORT","5432")  # Default PostgreSQL port
DB_USER = os.getenv("DB_USER","ML-user")  # Default
DB_PASSWORD = os.getenv("DB_PASSWORD","123")
DB_NAME = os.getenv("DB_NAME","model_metrics_db")  # Default database name

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()