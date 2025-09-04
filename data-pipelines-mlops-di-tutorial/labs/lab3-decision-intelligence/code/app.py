import streamlit as st
import pandas as pd
import mlflow
import shap
import numpy as np
import os
import matplotlib.pyplot as plt

def load_model_and_explainer():
    """
    Loads the latest MLflow model and creates a SHAP explainer.
    """
    # This assumes the script is run from the `code` directory of lab3
    # and the mlruns directory is in the root of the project.
    mlflow_tracking_uri = "../../../mlruns"
    mlflow.set_tracking_uri(mlflow_tracking_uri)

    # Find the latest run
    runs = mlflow.search_runs()
    latest_run_id = runs.iloc[0]['run_id']

    # Load the model
    model_uri = f"runs:/{latest_run_id}/logistic_regression_model"
    model = mlflow.sklearn.load_model(model_uri)

    # Create a SHAP explainer
    # We need some background data for the explainer. We'll use the training data.
    processed_data_path = os.path.join(os.path.dirname(__file__), '../../lab1-data-pipelines/data/churn_processed.csv')
    df = pd.read_csv(processed_data_path)
    features = ['Age', 'Tenure', 'Balance', 'NumOfProducts', 'IsActiveMember', 'BalanceSalaryRatio']
    X = df[features]

    explainer = shap.LinearExplainer(model, X)

    return model, explainer, features

def main():
    st.title("Decision Intelligence: Customer Churn Prediction")

    st.write("""
    This application demonstrates how a machine learning model can be used to support decision-making.
    Enter customer details on the left to get a churn prediction and an explanation of the prediction.
    """)

    model, explainer, features = load_model_and_explainer()

    # Sidebar for user input
    st.sidebar.header("Customer Details")

    age = st.sidebar.slider("Age", 20, 80, 40)
    tenure = st.sidebar.slider("Tenure (years)", 0, 10, 5)
    balance = st.sidebar.number_input("Balance", 0.0, 250000.0, 100000.0)
    num_products = st.sidebar.slider("Number of Products", 1, 4, 1)
    is_active_member = st.sidebar.selectbox("Is Active Member?", (0, 1))
    estimated_salary = st.sidebar.number_input("Estimated Salary", 0.0, 200000.0, 100000.0)

    # Create a dataframe for prediction
    balance_salary_ratio = balance / (estimated_salary + 0.01)
    input_data = pd.DataFrame({
        'Age': [age],
        'Tenure': [tenure],
        'Balance': [balance],
        'NumOfProducts': [num_products],
        'IsActiveMember': [is_active_member],
        'BalanceSalaryRatio': [balance_salary_ratio]
    })

    # Predict and explain
    if st.sidebar.button("Predict Churn"):
        prediction = model.predict(input_data)[0]
        prediction_proba = model.predict_proba(input_data)[0]

        st.subheader("Prediction")
        if prediction == 1:
            st.warning("This customer is likely to CHURN.")
        else:
            st.success("This customer is likely to STAY.")

        st.write(f"Probability of Churn: {prediction_proba[1]:.2f}")
        st.write(f"Probability of Staying: {prediction_proba[0]:.2f}")

        # SHAP Explanation
        st.subheader("Prediction Explanation")
        shap_values = explainer.shap_values(input_data)

        fig, ax = plt.subplots()
        shap.force_plot(explainer.expected_value, shap_values[0,:], input_data.iloc[0,:], matplotlib=True, show=False)
        st.pyplot(fig, bbox_inches='tight')

        st.write("""
        **How to read this chart:**
        - The **base value** is the average prediction over the entire dataset.
        - **Features in red** are pushing the prediction higher (towards churn).
        - **Features in blue** are pushing the prediction lower (towards staying).
        - The size of the bar represents the magnitude of the feature's impact.
        """)

if __name__ == "__main__":
    main()
