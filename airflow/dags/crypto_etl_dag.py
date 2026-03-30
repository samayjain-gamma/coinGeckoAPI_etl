from datetime import datetime

from airflow.providers.standard.operators.python import PythonOperator

from airflow import DAG


def extract():
    print("Extract running")


def transform():
    print("Transform running")


def load():
    print("Load running")


with DAG(
    dag_id="crypto_pipeline_test",
    start_date=datetime(2024, 1, 1),
    schedule="*/5 * * * *",
    catchup=False,
) as dag:

    extract_task = PythonOperator(task_id="extract", python_callable=extract)

    transform_task = PythonOperator(task_id="transform", python_callable=transform)

    load_task = PythonOperator(task_id="load", python_callable=load)

    extract_task >> transform_task >> load_task
