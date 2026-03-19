from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from datetime import datetime, timedelta

default_args = {
    "owner"           : "airflow",
    "depends_on_past" : False,
    "retries"         : 1,
    "retry_delay"     : timedelta(minutes=5),
}

# ── Update these 3 paths to match your workspace ──
BRONZE_PATH = "/Workspace/Users/smiles081102@gmail.com/energy-consumption-etl-pipeline/bronze/bronze_ingestion"
SILVER_PATH = "/Workspace/Users/smiles081102@gmail.com/energy-consumption-etl-pipeline/silver/silver_layer"
GOLD_PATH   = "/Workspace/Users/smiles081102@gmail.com/energy-consumption-etl-pipeline/Gold/gold_layer"

with DAG(
    dag_id            = "energy_consumption_etl",
    default_args      = default_args,
    start_date        = datetime(2026, 3, 14),
    schedule_interval = "0 4 * * *",
    catchup           = False,
    tags              = ["databricks", "etl", "energy", "medallion"]
) as dag:

    raw_data_ingestion = DatabricksSubmitRunOperator(
        task_id            = "raw_data_ingestion",
        databricks_conn_id = "databricks_default",
        json={
            "run_name": "bronze_{{ ds }}",
            "tasks": [
                {
                    "task_key"       : "bronze_ingestion",
                    "notebook_task"  : {
                        "notebook_path"  : BRONZE_PATH,
                        "base_parameters": {
                            "run_date": "{{ ds }}",
                            "env"     : "prod"
                        }
                    }
                }
            ]
        },
        wait_for_termination   = True,
        polling_period_seconds = 30,
    )

    silver_transformation = DatabricksSubmitRunOperator(
        task_id            = "silver_transformation",
        databricks_conn_id = "databricks_default",
        json={
            "run_name": "silver_{{ ds }}",
            "tasks": [
                {
                    "task_key"     : "silver_transformation",
                    "notebook_task": {
                        "notebook_path"  : SILVER_PATH,
                        "base_parameters": {
                            "run_date": "{{ ds }}",
                            "env"     : "prod"
                        }
                    }
                }
            ]
        },
        wait_for_termination   = True,
        polling_period_seconds = 30,
    )

    analytic_features = DatabricksSubmitRunOperator(
        task_id            = "analytic_features",
        databricks_conn_id = "databricks_default",
        json={
            "run_name": "gold_{{ ds }}",
            "tasks": [
                {
                    "task_key"     : "gold_layer",
                    "notebook_task": {
                        "notebook_path"  : GOLD_PATH,
                        "base_parameters": {
                            "run_date": "{{ ds }}",
                            "env"     : "prod"
                        }
                    }
                }
            ]
        },
        wait_for_termination   = True,
        polling_period_seconds = 30,
    )

    raw_data_ingestion >> silver_transformation >> analytic_features