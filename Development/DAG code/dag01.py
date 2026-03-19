from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from datetime import datetime, timedelta

default_args = {
    "owner"           : "airflow",
    "depends_on_past" : False,
    "retries"         : 1,
    "retry_delay"     : timedelta(minutes=5),
}

with DAG(
    dag_id            = "energy_consumption",
    default_args      = default_args,
    start_date        = datetime(2026, 3, 14),
    schedule_interval = "0 4 * * *",
    catchup           = False,
    tags              = ["databricks", "etl", "energy", "medallion"]
) as dag:

    run_pipeline = DatabricksRunNowOperator(
        task_id                = "energy_consumption_etl",
        databricks_conn_id     = "databricks_default",
        job_id                 = 1030990226120278,
        wait_for_termination   = True,
        polling_period_seconds = 30,
    )

    run_pipeline
