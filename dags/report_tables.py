"""DAG that runs a transformation on data in DuckDB using the Astro SDK"""

# --------------- #
# PACKAGE IMPORTS #
# --------------- #

from airflow.decorators import dag
from pendulum import datetime

# import tools from the Astro SDK
from astro import sql as aql
from astro.sql.table import Table

# -------------------- #
# Local module imports #
# -------------------- #

from include.global_variables import global_variables as gv

# ----------------- #
# Astro SDK Queries #
# ----------------- #

@aql.dataframe(pool="duckdb")
def transformation_logic(in_table: pd.Dataframe):
    #  print ingested df to logs
    gv.task_log.info(in_table)

    # import transformation function here

    # print result table to the logs
    gv.task_log.info(output_df)
    return output_df


@dag(
    start_date=datetime(2023,1,1)
)
def create_result_dfs(
    in_table=Table(name=c.)
)