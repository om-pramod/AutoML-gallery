# Lab 3: From Predictions to Decisions with Decision Intelligence

Welcome to the final lab! In this lab, we will explore the concept of Decision Intelligence and build a simple interactive application to see how machine learning models can be used to make better, data-driven decisions.

## What is Decision Intelligence?

Decision Intelligence (DI) is an emerging field that combines data science, social science, and managerial science to improve decision-making. It's not just about making predictions; it's about understanding the context of the decision, the potential outcomes, and the "why" behind the model's recommendations.

Key components of Decision Intelligence include:
- **Predictive Models:** The machine learning models that provide predictions (which we built in Lab 2).
- **Explainability (XAI):** Techniques to understand why a model made a certain prediction. This builds trust and provides deeper insights.
- **Simulation and Optimization:** Exploring different scenarios to find the best course of action.
- **Human-in-the-loop:** Creating tools that augment human decision-makers, not replace them.

In this lab, we will focus on building an interactive tool with model explainability.

## Hands-On: Building a Decision Support App with Streamlit and SHAP

We will build a web application using Streamlit that allows a user (e.g., a bank manager) to input customer details, get a churn prediction from our model, and see an explanation for that prediction using SHAP.

### Prerequisites

- Python 3.6+
- `streamlit`, `shap`, `matplotlib`. You can install them using pip:
  ```bash
  pip install streamlit shap matplotlib
  ```
- Completion of Lab 2. You must have the `mlruns` directory from running the training script.

### Steps

1. **Understand the Application Script:**
   The Python script `code/app.py` contains the code for our Streamlit application. It does the following:
   - Loads the latest churn prediction model you trained with MLflow in Lab 2.
   - Creates a SHAP explainer to interpret the model's predictions.
   - Builds a user interface with Streamlit that allows you to input customer data.
   - Displays the model's prediction (Churn or Stay) and a SHAP force plot to explain the prediction.

2. **Run the Streamlit Application:**
   Navigate to the `code` directory of this lab in your terminal and run the app:
   ```bash
   cd code
   streamlit run app.py
   ```
   This will start the Streamlit server and open the application in your web browser.

3. **Interact with the App:**
   - Use the sliders and input boxes in the sidebar to change the customer's details.
   - Click the "Predict Churn" button to see the model's prediction.
   - Analyze the SHAP plot to understand which features are influencing the prediction for the specific customer you defined.

## Conclusion

Congratulations on completing the tutorial! You have now gone through the entire lifecycle, from building a data pipeline, to training and tracking a model, and finally to building a decision intelligence tool.

This simple application shows the power of moving beyond just predictions. By providing explanations, we can empower users to make more informed and confident decisions. This is the core idea behind Decision Intelligence.

From here, you can explore more advanced topics like:
- Deploying the Streamlit app to the cloud.
- Automating the entire pipeline from data processing to model deployment (CI/CD for ML).
- Monitoring the model's performance over time.
