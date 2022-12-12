from datetime import timedelta


# Importing Airflow libraries.
from airflow import utils
from airflow.models import Variable
from airflow.decorators import dag, task

from utils.aws.lambda_funcs import LambdaFuncs
from utils.airflow_dependencies.airflow_variables import AirflowVariables


# Defining constants. Defining the DAG name.
DAG_NAME = "etl_currency"
DAG_NAME_PARAMS = "_".join([DAG_NAME, "params"])

PARAMS = Variable.get(
    key=DAG_NAME_PARAMS,
    default_var=False,
    deserialize_json=True
    )


# Capturing the arguments needed to execute the DAG.

default_args = {
    "owner"           : "Luis Felipe A. Nogueira",
    "start_date"      : utils.dates.days_ago(0),
    "depends_on_past" : False,
    "email"           : ["."],
    "email_on_failure": False,
    "email_on_retry"  : False,
    "retries"         : 0,
    "retry_delay"     : timedelta(minutes = int(PARAMS['timeout'])),
    "catchup"         : False
}


doc_md = """

### Currency ETL

#### Purpose

This DAG invokes a lambda function on AWS that will request data from an API,
then load it in a pandas dataframe and finally insert into a table in Redshift.

"""

dag_params = {
    "dag_id"           : DAG_NAME,
    "schedule_interval": PARAMS['schedule_interval'],
    "dagrun_timeout"   : timedelta(minutes = int(PARAMS['timeout'])),
    "catchup"          : False,
    "default_args"     : default_args,
    "max_active_runs"  : 1,
    "tags":["data_warehouse", "extraction", "apis"],
    "doc_md": doc_md
}


# Creating the DAG.
@dag(**dag_params)
def taskflow():

    @task(task_id="send_usd-brl_to_redshift")
    def send_user_activity_results_to_redshift():
        
        payload = PARAMS['lambda_payload']
        LambdaFuncs.invoke_lambda(lambda_payload=payload)

    @task(task_id="update_time_interval")
    def update_time_interval():

        AirflowVariables.update_interval(dag_name_params=DAG_NAME_PARAMS)

    # [Workflow] Defining the DAG tasks workflow.
    send_user_activity_results_to_redshift()  >> update_time_interval()

dag = taskflow()
