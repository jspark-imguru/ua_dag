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
    'test_imguru',
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
    application_file="t0_customer.yaml",
    dag=dag,
    api_group="sparkoperator.hpe.com",
    enable_impersonation_from_ldap_user=True    
)

t0_salehistory_store = SparkKubernetesOperator(
    task_id='t0_salehistory_store',
    namespace="spark",
    application_file="t0_salehistory.yaml",
    dag=dag,
    api_group="sparkoperator.hpe.com",
    enable_impersonation_from_ldap_user=True    
)

t1_customer_transform = SparkKubernetesOperator(
    task_id='t1_customer_transform',
    namespace="spark",
    application_file="t1_transform.yaml",
    dag=dag,
    api_group="sparkoperator.hpe.com",
    enable_impersonation_from_ldap_user=True    
)

t2_data_merge = SparkKubernetesOperator(
    task_id='t2_data_merge',
    namespace="spark",
    application_file="t2_datamerge.yaml",
    dag=dag,
    api_group="sparkoperator.hpe.com",
    enable_impersonation_from_ldap_user=True    
)

t0_customer_store >> t1_customer_transform >> t2_data_merge
t0_salehistory_store >> t2_data_merge