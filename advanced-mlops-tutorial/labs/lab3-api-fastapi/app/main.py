import pandas as pd
import mlflow
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pybreaker import CircuitBreaker
import os

# --- Configuration ---
# It's better to load the MLflow tracking URI from an environment variable in a real app
# For this tutorial, we'll hardcode it, assuming the app is run from its directory.
MLFLOW_TRACKING_URI = "../../../mlruns"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
MODEL_NAME = "churn-classifier"
MODEL_STAGE = "Production" # We will load the model from the "Production" stage

# --- Pydantic Model for Input Validation ---
class CustomerFeatures(BaseModel):
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float
    # Add other features your model expects, except the one you engineer
    Gender: str
    Geography: str

    # Example of adding a default value
    # BalanceSalaryRatio: float = 0.0

# --- Model Loading with Circuit Breaker ---
# The circuit breaker will prevent the app from repeatedly trying to load the model if MLflow is down.
model_breaker = CircuitBreaker(fail_max=3, reset_timeout=60)
model = None

@model_breaker
def load_model():
    """Loads the model from MLflow Model Registry. Protected by a circuit breaker."""
    global model
    try:
        model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
        model = mlflow.pyfunc.load_model(model_uri)
        print(f"Successfully loaded model '{MODEL_NAME}' version from stage '{MODEL_STAGE}'")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise  # Re-raise the exception to trip the circuit breaker

# --- FastAPI Application ---
app = FastAPI(
    title="Churn Prediction API",
    description="An API to predict customer churn using a model from the MLflow Registry.",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    """Load the model during startup."""
    print("Attempting to load model on startup...")
    try:
        load_model()
    except Exception as e:
        print(f"Startup model loading failed: {e}")
        # The app will still start, but the /predict endpoint will fail until the model is loaded.

@app.get("/", tags=["Health Check"])
def read_root():
    """Root endpoint for health check."""
    return {"status": "API is running"}

@app.post("/predict", tags=["Prediction"])
def predict_churn(features: CustomerFeatures):
    """
    Predicts customer churn based on input features.
    """
    global model
    if model is None:
        # Try to load the model again if it failed on startup
        try:
            print("Model not loaded. Attempting to load now...")
            load_model()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Service Unavailable: Model could not be loaded. Error: {e}")

    try:
        # 1. Convert Pydantic model to dictionary
        input_dict = features.dict()

        # 2. Engineer the 'BalanceSalaryRatio' feature
        # This must match the feature engineering in your training pipeline
        input_dict['BalanceSalaryRatio'] = input_dict['Balance'] / (input_dict['EstimatedSalary'] + 0.01)

        # 3. Convert to pandas DataFrame
        # The model expects a DataFrame as input
        input_df = pd.DataFrame([input_dict])

        # 4. Make prediction
        prediction = model.predict(input_df)

        # The output of predict() is often a numpy array
        churn_status = "Churn" if int(prediction[0]) == 1 else "Stay"

        return {
            "prediction": churn_status,
            "prediction_label": int(prediction[0])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# To run this app:
# 1. Navigate to this directory in your terminal.
# 2. Run: uvicorn main:app --reload
