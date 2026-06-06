from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import subprocess
import sys
import os

default_args = {
    "owner": "orderwave",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "ecommerce_pipeline",
    default_args=default_args,
    description="OrderWave daily ingestion pipeline",
    schedule_interval="0 6 * * *",
    catchup=False,
    tags=["orderwave"],
)

def run_script(script_path):
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        env={**os.environ, "PG_HOST": "postgres", "PG_PORT": "5432"}
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Script failed:\n{result.stderr}")

def ingest_orders():
    run_script("/opt/airflow/ingestion/ingest_orders.py")

def ingest_products():
    run_script("/opt/airflow/ingestion/ingest_products.py")

def ingest_inventory():
    run_script("/opt/airflow/ingestion/ingest_inventory.py")

t1 = PythonOperator(
    task_id="ingest_orders",
    python_callable=ingest_orders,
    dag=dag,
)

t2 = PythonOperator(
    task_id="ingest_products",
    python_callable=ingest_products,
    dag=dag,
)

t3 = PythonOperator(
    task_id="ingest_inventory",
    python_callable=ingest_inventory,
    dag=dag,
)

t1 >> t2 >> t3