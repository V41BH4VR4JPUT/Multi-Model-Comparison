from database import engine
from models_db import ModelMetrics

# Create the table
ModelMetrics.__table__.create(bind=engine, checkfirst=True)
