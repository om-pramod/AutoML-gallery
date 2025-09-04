import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn
import os

def train_model():
    """
    This function trains a model, logs it with MLflow, and saves it.
    """
    # Note: This script assumes that Lab 1 has been completed and
    # the processed data is available.
    # The path is relative to this script's location.
    processed_data_path = os.path.join(os.path.dirname(__file__), '../../lab1-data-pipelines/data/churn_processed.csv')

    # Load the processed data
    try:
        df = pd.read_csv(processed_data_path)
    except FileNotFoundError:
        print(f"Error: Processed data not found at {processed_data_path}")
        print("Please make sure you have run the pipeline from Lab 1.")
        return

    # Define features (X) and target (y)
    # For simplicity, we will use a subset of features.
    features = ['Age', 'Tenure', 'Balance', 'NumOfProducts', 'IsActiveMember', 'BalanceSalaryRatio']
    X = df[features]
    y = df['Exited']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Start an MLflow run
    with mlflow.start_run():
        # Train a Logistic Regression model
        # You can experiment with different parameters
        C = 1.0
        solver = 'liblinear'
        model = LogisticRegression(C=C, solver=solver, random_state=42)
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        # Log parameters and metrics
        mlflow.log_param("C", C)
        mlflow.log_param("solver", solver)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        # Log the model
        mlflow.sklearn.log_model(model, "logistic_regression_model")

        print("Model trained and logged successfully.")
        print(f"To see the results, run 'mlflow ui' in your terminal in the 'data-pipelines-mlops-di-tutorial' directory.")


if __name__ == "__main__":
    train_model()
