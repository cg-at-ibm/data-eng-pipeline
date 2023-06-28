from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from plugins.helpers import SqlQueries

class CreateTablesOperator(BaseOperator):
    ui_color = '#355681'

    table_queries = {
        "staging_events_table": (SqlQueries.staging_events_table_drop, SqlQueries.staging_events_table_create),
        "staging_songs_table": (SqlQueries.staging_songs_table_drop, SqlQueries.staging_songs_table_create),
        "songplays_table": (SqlQueries.songplay_table_drop, SqlQueries.songplay_table_create),
        "users_table": (SqlQueries.user_table_drop, SqlQueries.user_table_create),
        "songs_table": (SqlQueries.song_table_drop, SqlQueries.song_table_create),
        "artists_table": (SqlQueries.artist_table_drop, SqlQueries.artist_table_create),
        "time_table": (SqlQueries.time_table_drop, SqlQueries.time_table_create)
    }

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 tables,
                 *args, **kwargs):

        super(CreateTablesOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables

    def execute(self, context):
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        for table in self.tables:
            if table not in self.table_queries:
                self.log.error(f'CreateTablesOperator: Unsupported table {table}. Skipping.')
                continue

            sql_drop_table, sql_create_table = self.table_queries[table]

            self.log.info(f'CreateTablesOperator: Dropping table {table} if it exists.')
            redshift_hook.run(sql_drop_table)
            
            self.log.info(f'CreateTablesOperator: Creating table {table}.')
            redshift_hook.run(sql_create_table)

            self.log.info(f'CreateTablesOperator: Table {table} created successfully.')