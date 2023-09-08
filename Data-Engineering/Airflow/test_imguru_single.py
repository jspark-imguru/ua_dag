from airflow import DAG
from airflow.models.param import Param
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'max_active_runs': 1,
    'retries': 0
}

dag = DAG(
    'test_imguru_single',
    default_args=default_args,
    schedule_interval=None,
    tags=['imguru', 'spark'],
    params={
        'airgap_registry_url': Param("", type=["null", "string"], pattern=r"^$|^\S+/$")
    },
    render_template_as_native_obj=True
)

t0_customer_store = SparkKubernetesOperator(
    task_id='t0_customer_store',
    namespace="spark",
    application_file="t0_table_customer_test.yaml",
    dag=dag,
    api_group="sparkoperator.hpe.com",
    enable_impersonation_from_ldap_user=True    
)

t0_customer_store