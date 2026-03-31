import asyncio
from datetime import datetime

from airflow.providers.standard.operators.python import PythonOperator

from airflow import DAG
from coingecko.alerts.alert_service import process_prize_alert
from coingecko.extract.extract_data import fetch_top_50_cryptos
from coingecko.load.load_to_db import load_to_db
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


def load_task(**context):
    ti = context["ti"]

    normalized_data = ti.xcom_pull(task_ids="normalize_task")

    loaded_data = asyncio.run(load_to_db(normalized_data=normalized_data))
    return loaded_data


def alert_task(**context):
    ti = context["ti"]

    load_result = ti.xcom_pull(task_ids="load_task")

    alerts = load_result

    process_prize_alert(alerts)


with DAG(
    dag_id="crypto_price_pipeline",
    start_date=datetime(2026, 3, 30, 10, 0),
    schedule="*/3 * * * *",
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

    load_data = PythonOperator(task_id="load_data", python_callable=load_task)

    send_alerts = PythonOperator(task_id="send_alerts", python_callable=alert_task)

    extract >> clean >> normalize >> load_data >> send_alerts
