from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.secrets.metastore import MetastoreBackend
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from plugins.helpers import SqlQueries
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    template_fields = ("s3_key",)
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        format as json 'auto ignorecase'
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 delimiter=",",
                 ignore_headers=1,
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.delimiter = delimiter
        self.ignore_headers = ignore_headers
        self.aws_credentials_id = aws_credentials_id

    def execute(self, context):
        self.log.info("Retrieving AWS credentials.")
        #aws_hook = AwsHook(self.aws_credentials_id)
        #credentials = aws_hook.get_credentials()    <-- Didn't work 
        #s3cred = S3Hook(aws_conn_id=self.aws_credentials_id, verify=False)
        #credentials = s3cred.get_credentials()
        metastoreBackend = MetastoreBackend()
        aws_connection=metastoreBackend.get_connection("aws_credentials")
        access_key = aws_connection.login
        secret_key = aws_connection.password


        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        if self.table == "staging_events_table":
            sql_drop_table = SqlQueries.staging_events_table_drop
            sql_create_table = SqlQueries.staging_events_table_create
        elif self.table == "staging_songs_table":
            sql_drop_table = SqlQueries.staging_songs_table_drop
            sql_create_table = SqlQueries.staging_songs_table_create
        else:
            raise ValueError(f"Table not supported: {self.table}")

        #self.log.info("Clearing data from destination Redshift table")
        #redshift_hook.run("DELETE FROM {}".format(self.table))

        self.log.info("Copying data from S3 to Redshift")
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            s3_path,
            access_key,
            secret_key,
        )

        # Load data from S3
        self.log.info("Loading data from S3 into Redshift.")
        redshift_hook.run(formatted_sql)
        self.log.info("Data loading completed.")