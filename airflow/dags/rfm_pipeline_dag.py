from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "data_engineer",
    "retries": 1
}

with DAG(
    dag_id="rfm_customer_segmentation_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args
) as dag:

    create_schema = BashOperator(
    task_id="create_schema",
    bash_command="psql postgresql://rfm_user:rfm_pass@postgres:5432/rfm_analytics -f /opt/airflow/warehouse/schema.sql"
    )

    ingest = BashOperator(
        task_id="ingest_transactions",
        bash_command="python /opt/airflow/ingestion/batch_ingest.py"
    )

    transform = BashOperator(
        task_id="calculate_rfm",
        bash_command="psql postgresql://rfm_user:rfm_pass@postgres:5432/rfm_analytics -f /opt/airflow/transformations/rfm_transform.sql"
    )

    segment = BashOperator(
        task_id="run_kmeans",
        bash_command="python /opt/airflow/ml/kmeans_segmentation.py"
    )

    generate_data = BashOperator(
    task_id="generate_transactions",
    bash_command="python /opt/airflow/data_generator/generate_transactions.py"
    )

create_schema >> generate_data >> ingest >> transform >> segment
    
