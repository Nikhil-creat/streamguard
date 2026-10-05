from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG("streamguard_batch", start_date=datetime(2026, 1, 1), schedule="@hourly", catchup=False) as dag:
    compact = BashOperator(task_id="delta_optimize", bash_command="python -c \"from deltalake import DeltaTable as D; D('s3://lake/bronze/txn').optimize.compact()\"")
    silver = BashOperator(task_id="dbt_run", bash_command="cd /opt/dbt && dbt run && dbt test")
    retrain = BashOperator(task_id="retrain_cnn", bash_command="echo 'retrain CNN on confirmed fraud labels'")
    drift = BashOperator(task_id="drift_check", bash_command="python /opt/airflow/ml/drift.py")
    compact >> silver >> drift >> retrain
