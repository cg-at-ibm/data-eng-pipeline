from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from plugins.helpers import SqlQueries

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    table_queries = {
       "user_table":SqlQueries.user_table_insert,
       "song_table":SqlQueries.song_table_insert,
       "artist_table":SqlQueries.artist_table_insert,
       "time_table":SqlQueries.time_table_insert
    }

    @apply_defaults
    def __init__(self,
                redshift_conn_id="",
                table="",
                mode="delete-load",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.mode = mode

    def execute(self, context):
        self.log.info('Connecting to Redshift.')
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if self.table not in self.table_queries:
            self.log.error(f'Unsupported table {self.table}. Skipping.')
            return

        if self.mode == 'append-only':
            self.log.info(f'Loading data into {self.table} in append-only mode.')
        elif self.mode == 'delete-load':
            self.log.info(f'Clearing data from {self.table} and loading data in delete-load mode.')
            redshift_hook.run("DELETE FROM {}".format(self.table))
        else:
            self.log.error(f'Unsupported mode {self.mode}. Skipping.')
            return

        sql_load = self.table_queries[self.table]
        redshift_hook.run(sql_load)

        self.log.info(f'Data loaded into {self.table} successfully.')