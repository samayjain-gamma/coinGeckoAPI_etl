from datetime import datetime

from airflow.providers.standard.operators.python import PythonOperator

from airflow import DAG
from coingecko.extract.extract_data import fetch_top_50_cryptos
from coingecko.transform.clean_data import clean_crypto_data
from coingecko.transform.normalize_data import normalize_crypto_data


def extract_task(**context):
    data = fetch_top_50_cryptos()
    return data


def clean_task(**context):
    ti = context["ti"]

    raw_data = ti.xcom_pull(task_ids="extract_task")

    cleaned = clean_crypto_data(raw_data)

    return cleaned


def normalize_task(**context):
    ti = context["ti"]

    cleaned_data = ti.xcom_pull(task_ids="clean_task")

    normalized = normalize_crypto_data(cleaned_data)

    return normalized


def dummy_task_1():
    print("Dummy task 1 executed")


def dummy_task_2():
    print("Dummy task 2 executed")


with DAG(
    dag_id="crypto_price_pipeline",
    start_date=datetime(2026, 3, 30, 10, 0),
    schedule="*/2 * * * *",
    catchup=False,
    tags=["crypto", "etl"],
) as dag:

    extract = PythonOperator(
        task_id="extract_task",
        python_callable=extract_task,
    )

    clean = PythonOperator(
        task_id="clean_task",
        python_callable=clean_task,
    )

    normalize = PythonOperator(
        task_id="normalize_task",
        python_callable=normalize_task,
    )

    dummy1 = PythonOperator(
        task_id="dummy_task_1",
        python_callable=dummy_task_1,
    )

    dummy2 = PythonOperator(
        task_id="dummy_task_2",
        python_callable=dummy_task_2,
    )

    extract >> clean >> normalize >> dummy1 >> dummy2
