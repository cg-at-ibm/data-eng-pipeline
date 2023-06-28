This repository contains an airflow workspace that is used to execute a data pipeline that automatically loads data from an S3 object and stores it in a AWS Redshift data warehouse.

### File structure

.			      # Home directory. Also set PYTHONPATH to this directory so modules are loaded properly.

├── airflow                   # AIRFLOW_HOME (use this directory for airflow installation.)

├── dags                      # Contains the DAG for running the pipeline

├── plugins                   # Plugin directory

├───── helpers	              # SQL queries used by operators for interacting with RedShift

├───── operators              # Operators used for DAG pipeline

└── README.md

### Notes for testing the code:
To replicate the settings/installation used by the project:

1) Navigate to airflow folder and then:

export AIRFLOW_HOME=$(pwd)

sudo pip install 'apache-airflow[amazon]'

pip install kubernetes

pip install apache-airflow-providers-postgres 


3) Copy the airflow.cfg file from this repository into the airflow folder

4) Set Python Path to the home directory by navigating to home folder and then:
export PYTHONPATH="$PYTHONPATH:$(pwd)"
echo 'export PYTHONPATH="$PYTHONPATH:$(pwd)"' >> ~/.bashrc
source ~/.bashrc
