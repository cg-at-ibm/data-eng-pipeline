import os
from datetime import datetime, timedelta
import pendulum

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from operators import StageToRedshiftOperator, LoadFactOperator, LoadDimensionOperator, DataQualityOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

s3_bucket = 'udacity-dend'
s3_events = 'log-data'
s3_songs = 'song-data/A/A/A'

default_args = {
    'owner': 'cg-at-ibm',
    'start_date': datetime(2023, 6, 28),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_failure': False
}

# Data quality checks defined in the DAG
dq_checks=[
        {'check_sql': "SELECT COUNT(*) FROM songplay_table WHERE songplay_id is null", 'expected_result': 0},
        {'check_sql': "SELECT COUNT(*) FROM user_table WHERE userid is null", 'expected_result': 0},
        {'check_sql': "SELECT COUNT(*) FROM song_table WHERE song_id is null", 'expected_result': 0},
        {'check_sql': "SELECT COUNT(*) FROM time_table WHERE start_time is null", 'expected_result': 0},
        {'check_sql': "SELECT COUNT(*) FROM artist_table WHERE artist_id is null", 'expected_result': 0}
    ]

#Instantiate a dag object
dag = DAG('data_pipeline',
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='0 * * * *',
    start_date=datetime(2023, 6, 28)   
)

#Starting dummy operator
start_operator = DummyOperator(task_id='Begin_execution', dag = dag)


#Stage events operator 
stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    redshift_conn_id = "redshift",
    table = "staging_events_table",
    s3_bucket=s3_bucket,
    s3_key=s3_events,
    dag=dag
)

#Stage songs operator
stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    redshift_conn_id = "redshift",
    table = "staging_songs_table",
    s3_bucket=s3_bucket,
    s3_key=s3_songs,
    dag=dag
)

#Load fact songplays operator
load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    redshift_conn_id="redshift",
    table='songplays_table',
    mode='append-only',
    dag=dag
)

#Load user dimension operator
load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    redshift_conn_id="redshift",
    table='user_table',
    mode='delete-load',
    dag=dag
)

#Load song dimension operator
load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    redshift_conn_id="redshift",
    table='song_table',
    mode='delete-load',
    dag=dag
)

#Load artist dimension operator
load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    redshift_conn_id="redshift",
    table='artist_table',
    mode='delete-load',
    dag=dag
)

#load time dimension operator
load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    redshift_conn_id="redshift",
    table='time_table',
    mode='delete-load',
    dag=dag
)

# Data quality check operator
run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    redshift_conn_id = "redshift",
    dq_checks = dq_checks,
    dag=dag
)

# Dummy end operator
end_operator = DummyOperator(task_id='Finish_execution', dag = dag)

#Defining the directionality of the operators
start_operator  >> [stage_events_to_redshift, stage_songs_to_redshift] 
[stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table 
[load_time_dimension_table, load_song_dimension_table, load_user_dimension_table, load_artist_dimension_table] << load_songplays_table
run_quality_checks << [load_song_dimension_table, load_user_dimension_table, load_artist_dimension_table, load_time_dimension_table]
end_operator << run_quality_checks

