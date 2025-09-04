import pandas as pd
import os

def run_pipeline():
    """
    This function simulates a simple data pipeline.
    It reads data, cleans it, and saves the processed data.
    """
    # Define file paths
    # The ../data path is relative to the location of the script
    data_path = os.path.join(os.path.dirname(__file__), '../data/churn_data.csv')
    processed_data_path = os.path.join(os.path.dirname(__file__), '../data/churn_processed.csv')

    # Read the data
    try:
        df = pd.read_csv(data_path)
        print("Successfully loaded data.")
    except FileNotFoundError:
        print(f"Error: The file was not found at {data_path}")
        return

    # Simple data cleaning and feature engineering
    print("Performing data cleaning and feature engineering...")
    # For simplicity, we'll just fill any potential missing values, though our sample has none.
    df.fillna(0, inplace=True)

    # Create a new feature: Balance to Salary ratio
    # Add a small epsilon to avoid division by zero
    df['BalanceSalaryRatio'] = df['Balance'] / (df['EstimatedSalary'] + 0.01)

    # Save the processed data
    df.to_csv(processed_data_path, index=False)
    print(f"Successfully saved processed data to {processed_data_path}")

if __name__ == "__main__":
    run_pipeline()
