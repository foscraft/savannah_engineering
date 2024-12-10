from airflow import DAG  # type: ignore
from airflow.operators.python_operator import PythonOperator  # type: ignore
from datetime import datetime
import subprocess
import os

BASEDIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name):
    script_path = os.path.join(BASEDIR, "scripts", script_name)
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script {script_path} not found")
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error running script {script_name}: {result.stderr}")
    print(f"Script {script_name} output:\n{result.stdout}")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 9),
    'retries': 1,
}

dag = DAG(
    'savannah_pipeline',
    default_args=default_args,
    description='ETL Pipeline for Claims and User Data',
    schedule_interval='0 * * * *', 
)

task_extract = PythonOperator(
    task_id='extract_data',
    python_callable=run_script,
    op_args=['extract_data.py'],  
    dag=dag,
)

task_clean = PythonOperator(
    task_id='clean_data',
    python_callable=run_script,
    op_args=['clean_data.py'],
    dag=dag,
)

task_generate_insights = PythonOperator(
    task_id='generate_insights',
    python_callable=run_script,
    op_args=['generate_insights.py'],
    dag=dag,
)

task_extract >> task_clean >> task_generate_insights
