const slides = [
    {
        title: "Welcome to the MLOps Tutorial!",
        points: [
            "Today, we'll build a production-ready MLOps stack from scratch.",
            "We will cover the entire lifecycle: from data to a deployed, monitored model.",
            "This guide will walk you through the key concepts and code for each lab.",
        ],
    },
    {
        title: "Lab 1: Scalable ETL with Prefect & Dask",
        points: [
            "**Goal:** Build a robust and scalable ETL (Extract, Transform, Load) pipeline.",
            "**Prefect:** A workflow orchestration tool to build, run, and monitor data pipelines.",
            "**Dask:** A flexible parallel computing library to scale Python code.",
            "We'll define our pipeline as a series of tasks orchestrated by a flow."
        ],
    },
    {
        title: "Lab 1: Defining the 'Extract' Task",
        points: [
            "The first step is to read the raw data from our CSV file.",
            "We define a Prefect `@task` to handle this operation.",
        ],
        code: `
import pandas as pd
from prefect import task, flow

@task
def extract(path: str) -> pd.DataFrame:
    """Reads raw data from a CSV file."""
    df = pd.read_csv(path)
    return df`
    },
    {
        title: "Lab 1: 'Transform' Task with Dask",
        points: [
            "We use Dask to parallelize the transformation for speed.",
            "Convert pandas DataFrame to a Dask DataFrame.",
            "Perform transformations (e.g., feature engineering).",
            "Convert back to pandas DataFrame by calling `.compute()`."
        ],
        code: `
import dask.dataframe as dd

@task
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Transforms the data using Dask."""
    dask_df = dd.from_pandas(df, npartitions=4)

    dask_df['BalanceSalaryRatio'] = dask_df['Balance'] / (dask_df['EstimatedSalary'] + 0.01)

    processed_df = dask_df.compute()
    return processed_df`
    },
    {
        title: "Lab 1: The Complete ETL Flow",
        points: [
            "A Prefect `@flow` is a function that calls our tasks in order.",
            "This defines the entire dependency graph of our pipeline.",
        ],
        code: `
@flow(name="ETL Pipeline Flow")
def etl_flow():
    raw_df = extract('../../data/churn_data.csv')
    transformed_df = transform(raw_df)
    load(transformed_df, '../../data/churn_processed.parquet')

# To run the flow
if __name__ == "__main__":
    etl_flow()`
    },
    {
        title: "Lab 2: AutoML with PyCaret & MLflow",
        points: [
            "**Goal:** Automatically find the best model without manual tuning.",
            "**PyCaret:** A low-code AutoML library that simplifies model training.",
            "**MLflow:** Used to automatically track every experiment PyCaret runs.",
            "We will load our processed data and let PyCaret do the hard work."
        ],
    },
    {
        title: "Lab 2: Setting Up the Experiment",
        points: [
            "The `setup()` function initializes the environment.",
            "It handles preprocessing and sets up MLflow logging automatically.",
        ],
        code: `
from pycaret.classification import *
import mlflow

mlflow.set_tracking_uri('../../mlruns')

exp = setup(
    data=df,
    target='Exited',
    session_id=123,
    log_experiment=True,
    experiment_name='churn_prediction_automl'
)`
    },
    {
        title: "Lab 2: Comparing All Models",
        points: [
            "The `compare_models()` function is the core of PyCaret.",
            "It trains, cross-validates, and evaluates over a dozen models.",
            "It presents the results in a sortable grid to easily find the best one.",
        ],
        code: `
# This single line trains and evaluates multiple models
best_model = compare_models()`
    },
    {
        title: "Lab 2: Registering the Model",
        points: [
            "After finding the best model, we register it in the MLflow Model Registry.",
            "This makes the model available for deployment.",
        ],
        code: `
# Finalize the model (retrains on the full dataset)
final_model = finalize_model(best_model)

# Register the model in MLflow
mlflow.register_model(
    model_uri=f"runs:/{get_config('mlflow_run_id')}/model",
    name="churn-classifier"
)`
    },
    {
        title: "Lab 3: Deploying with FastAPI",
        points: [
            "**Goal:** Deploy our best model as a production-ready API.",
            "**FastAPI:** A high-performance web framework for building APIs.",
            "**Circuit Breaker:** A design pattern to make our API resilient to failures (e.g., if the model server is down).",
        ],
    },
    {
        title: "Lab 3: Preparing the Model",
        points: [
            "Before running the API, we must promote our model to the 'Production' stage.",
            "1. Go to the MLflow UI -> Models tab.",
            "2. Select the `churn-classifier` model.",
            "3. Find the latest version and use the 'Stage' dropdown to transition it to 'Production'."
        ],
    },
    {
        title: "Lab 3: FastAPI Application Structure",
        points: [
            "Our API code is in `app/main.py`.",
            "**Pydantic Model:** Defines the structure and data types for the API input.",
            "**Model Loading:** A function to load the model from MLflow, protected by a circuit breaker.",
            "**Prediction Endpoint:** The `/predict` endpoint that receives data, processes it, and returns a prediction.",
        ],
        code: `
# To run the API server:
# 1. cd advanced-mlops-tutorial/labs/lab3-api-fastapi/app
# 2. uvicorn main:app --reload

# Then open http://localhost:8000/docs in your browser.`
    },
    {
        title: "Lab 4: Monitoring & Drift Detection",
        points: [
            "**Goal:** Ensure our model remains accurate over time.",
            "**Model Drift:** The degradation of model performance due to changes in data or concepts.",
            "**Evidently AI:** An open-source tool to analyze and monitor ML models for drift.",
        ],
    },
    {
        title: "Lab 4: Generating a Drift Report",
        points: [
            "We compare our original training data (reference) with new data (current).",
            "Evidently generates an interactive report showing which features have drifted.",
        ],
        code: `
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# reference_df = original training data
# current_df = new production data

data_drift_report = Report(metrics=[DataDriftPreset()])
data_drift_report.run(reference_data=reference_df, current_data=current_df)

# This will display the report in the notebook
data_drift_report`
    },
    {
        title: "Lab 4: Automated Retraining Strategy",
        points: [
            "We can close the MLOps loop with automated retraining.",
            "1. **Monitor:** A scheduled job runs the drift report.",
            "2. **Detect:** If drift is detected above a threshold...",
            "3. **Trigger:** The job triggers our Prefect ETL flow (Lab 1).",
            "4. **Retrain:** The ETL output is used to run our AutoML process (Lab 2), which registers a new model version.",
            "This ensures our model stays up-to-date automatically."
        ],
    },
    {
        title: "Congratulations!",
        points: [
            "You have now designed a complete, end-to-end MLOps stack.",
            "You've covered Data Pipelines, AutoML, API Deployment, and Monitoring.",
            "These are the core skills used by top AI teams to build real-world systems.",
            "Thank you for attending!"
        ],
    }
];
