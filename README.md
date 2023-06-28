## Project

This repository contains an airflow workspace that is used to execute a data pipeline that automatically loads data from an S3 object and stores it in a AWS Redshift data warehouse.
The readme has been adapted from https://github.com/jaycode/udacity-data_pipelines


## How to run project locally

### 0. Create tables on the Redshift cluster

Run airflow/create_tables.sql on the Redshift cluster to create all the required tables.

### 1. Clone directory in your home folder and install required files

git clone https://github.com/cg-at-ibm/data-eng-pipeline.git
export AIRFLOW_HOME=$(pwd)
sudo pip install 'apache-airflow[amazon]'
pip install kubernetes
pip install apache-airflow-providers-postgres 

### 2. Modify the airflow/airflow.cfg file
load_examples = False

dags_folder = some path/home/dags

plugins_folder = some path/home/plugins

lazy_load_plugins = False

### 3. Start airflow server (if it overwrites .cfg file then you may have to rewrite it again)
airflow standalone


### 4. Create connection settings
Open http://localhost:8080 on Google Chrome, then go to "Admin > Connections" menu. From there, create the following connections:

    AWS credentials:
        Conn Id: aws_credentials
        Login: Your AWS ACCESS KEY
        Password: Your AWS SECRET ACCESS KEY
    Redshift connection
        Conn Id: redshift
        Conn Type: redshift
        Host: Endpoint of your Redshift cluster
        Schema: dev
        Login: awsuser
        Password: Password for user when launching your Redshift cluster.
        Port: 5439


### 5. Run data_pipeline dag
Run data_pipeline dag in airflow

## File structure

```plaintext
.                   # Home directory. Also set PYTHONPATH to this directory so plugins can load properly and don't appear broken.
├── airflow         # AIRFLOW_HOME (use this directory for airflow installation.)
├── dags            # Contains the DAG for running the pipeline
├── plugins         # Plugin directory
│   ├── helpers     # SQL queries used by operators for interacting with RedShift
│   └── operators   # Operators used for DAG pipeline
└── README.md      
└── create_tables.sql  # SQL query for creating tables neccesary for this project
