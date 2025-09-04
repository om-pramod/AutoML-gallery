# Lab 1: Building Your First Data Pipeline

Welcome to the first lab of our tutorial series! In this lab, you will learn the fundamentals of data pipelines and build a simple one using Python and the `pandas` library.

## What is a Data Pipeline?

A data pipeline is a series of automated steps that move data from a source to a destination. During this process, the data is often transformed and enriched. Data pipelines are the backbone of most data-driven applications, from analytics dashboards to machine learning models.

The most common type of data pipeline is an **ETL (Extract, Transform, Load)** pipeline:
- **Extract:**  Data is extracted from a source (e.g., a database, an API, a CSV file).
- **Transform:** The extracted data is cleaned, validated, and transformed into a desired format. This can include anything from handling missing values to creating new features.
- **Load:** The transformed data is loaded into a destination (e.g., a data warehouse, a data lake, or another file).

## Hands-On: Building a Simple Data Pipeline

In this lab, we will build a simple data pipeline that processes customer churn data.

### Prerequisites

- Python 3.6+
- `pandas` library. You can install it using pip:
  ```bash
  pip install pandas
  ```

### Steps

1. **Explore the Data:**
   The raw data is located in `data/churn_data.csv`. It contains information about bank customers. Take a look at the file to understand its structure.

2. **Understand the Pipeline Script:**
   The Python script `code/pipeline.py` contains our simple data pipeline. Open the file and read through the code and comments to understand what each part does.

   The pipeline performs the following steps:
   - **Extract:** It reads the `churn_data.csv` file into a pandas DataFrame.
   - **Transform:** It performs a simple data cleaning step (filling missing values) and creates a new feature called `BalanceSalaryRatio`.
   - **Load:** It saves the processed DataFrame to a new CSV file called `churn_processed.csv` in the `data` directory.

3. **Run the Pipeline:**
   Navigate to the `code` directory in your terminal and run the script:
   ```bash
   cd code
   python pipeline.py
   ```

4. **Verify the Output:**
   After running the script, you should see a new file `churn_processed.csv` in the `data` directory. Open this file and observe the changes. You should see the new `BalanceSalaryRatio` column.

## Conclusion

Congratulations! You have successfully built and run your first data pipeline. While this is a simple example, it demonstrates the core concepts of ETL. In real-world scenarios, data pipelines can be much more complex, involving multiple data sources, complex transformations, and orchestration tools like Apache Airflow or Prefect to manage schedules and dependencies.

In the next lab, we will use the processed data from this pipeline to train a machine learning model.
