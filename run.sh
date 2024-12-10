#!/bin/bash

# Define the notebook and Python file paths
NOTEBOOK_PATH="./api_data_pipeline.ipynb"
PYTHON_FILE_PATH="./api_data_pipeline.py"

echo "Converting Jupyter notebook to Python file..."
jupyter nbconvert --to python $NOTEBOOK_PATH --output $PYTHON_FILE_PATH

echo "Triggering the Airflow DAG..."
airflow dags trigger api_data_pipeline

# Optionally, you can wait for the DAG to finish or monitor its status
# airflow dags list_runs -d api_data_pipeline
