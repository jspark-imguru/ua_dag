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
    'imguru-airflow-run',
    default_args=default_args,
    schedule_interval=None,
    tags=['imguru', 'spark', 'POC'],
    params={
        'airgap_registry_url': Param("", type=["null", "string"], pattern=r"^$|^\S+/$")
    },
    render_template_as_native_obj=True
)

t1_cus_info_test = SparkKubernetesOperator(
    task_id='t1-cus-info-test',
    namespace="spark",
    application_file="create-t1-cus-info-test.yaml",
    dag=dag,
    api_group="sparkoperator.hpe.com",
    enable_impersonation_from_ldap_user=True    
)

t2_cus_orders_test = SparkKubernetesOperator(
    task_id='t2-cus-orders-test',
    namespace="spark",
    application_file="create-t2-cus-orders-test.yaml",
    dag=dag,
    api_group="sparkoperator.hpe.com",
    enable_impersonation_from_ldap_user=True    
) 

t3_cus_merge_test = SparkKubernetesOperator(
    task_id='t2-cus-merge-test',
    namespace="spark",
    application_file="create-t2-cus-orders-test.yaml",
    dag=dag,
    api_group="sparkoperator.hpe.com",
    enable_impersonation_from_ldap_user=True    
) 

t1_cus_info_test >> t2_cus_orders_test >> t3_cus_merge_test
