from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define a simple Python function to print "Hello World"
def print_hello_world():
    print("Hello World from Python!")

# Define the DAG
with DAG(
    dag_id='bash_and_python_hello_world',
    start_date=datetime(2025, 5, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['hello', 'world'],
) as dag:

    # Task 1: Run a bash command to print "Hello World"
    bash_task = BashOperator(
        task_id='bash_hello_world',
        bash_command='echo "Hello World from Bash!"',
        executor_config={
            "KubernetesExecutor": {
                "image": "alpine:latest",  # or any image with `echo` shell
            }
        },
    )

    # Task 2: Run a Python function to print "Hello World"
    python_task = PythonOperator(
        task_id='python_hello_world',
        python_callable=print_hello_world,
        executor_config={
            "KubernetesExecutor": {
                "image": "python:3.9",  # ensure the image has necessary Python libs
            }
        },
    )

    # Set task dependencies
    bash_task >> python_task
