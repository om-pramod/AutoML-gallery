# Lab 2: Introduction to MLOps with MLflow

Welcome to Lab 2! In this lab, you will be introduced to the world of MLOps (Machine Learning Operations) and learn how to use a popular tool, MLflow, to track your machine learning experiments.

## What is MLOps?

MLOps is a set of practices that aims to deploy and maintain machine learning models in production reliably and efficiently. It is the intersection of Machine Learning, DevOps, and Data Engineering.

Key aspects of MLOps include:
- **Experiment Tracking:** Logging parameters, metrics, and artifacts for each model training run. This helps in comparing different experiments and reproducing results.
- **Model Versioning:** Keeping track of different versions of your models.
- **Model Deployment:** Serving your models for inference.
- **Monitoring:** Monitoring the performance of your models in production.

In this lab, we will focus on experiment tracking and model versioning using **MLflow**.

## Hands-On: Training and Tracking a Model with MLflow

In this lab, we will use the processed data from Lab 1 to train a churn prediction model and track the experiment using MLflow.

### Prerequisites

- Python 3.6+
- `pandas`, `scikit-learn`, `mlflow`. You can install them using pip:
  ```bash
  pip install pandas scikit-learn mlflow
  ```
- Completion of Lab 1.

### Steps

1. **Understand the Training Script:**
   The Python script `code/train.py` contains the code to train our model. Open the file and read through the code. It does the following:
   - Loads the `churn_processed.csv` data from Lab 1.
   - Splits the data into training and testing sets.
   - Trains a Logistic Regression model.
   - Uses `mlflow` to log the model's parameters (like `C` and `solver`), metrics (like accuracy), and the model itself.

2. **Run the Training Script:**
   Navigate to the `code` directory in your terminal and run the script:
   ```bash
   cd code
   python train.py
   ```
   When you run this script, MLflow will automatically create a directory called `mlruns` in the parent `data-pipelines-mlops-di-tutorial` directory to store the tracking data.

3. **Explore the MLflow UI:**
   MLflow provides a web-based UI to view and compare your experiments. To launch the UI, navigate to the root directory of the tutorial in your terminal (`data-pipelines-mlops-di-tutorial`) and run:
   ```bash
   mlflow ui
   ```
   This will start a local server. Open your web browser and go to `http://localhost:5000` (or the URL shown in your terminal).

   In the MLflow UI, you can:
   - See the experiment run you just executed.
   - Click on the run to see the parameters, metrics, and artifacts (including the saved model).
   - Compare different runs if you execute the script multiple times (perhaps with different parameters in `train.py`).

## Conclusion

You have now trained a model and used MLflow to track its parameters and performance. This is a crucial first step in MLOps. By systematically tracking your experiments, you can ensure reproducibility and make informed decisions about which model to deploy.

In the final lab, we will take the model you trained and build a simple application around it to demonstrate the principles of Decision Intelligence.
