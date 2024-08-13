"DAG that runs a transformation on data in DuckDB using the Astro SDK."

# --------------- #
# PACKAGE IMPORTS #
# --------------- #

from airflow.decorators import dag
from pendulum import datetime
import pandas as pd
import duckdb

# import tools from the Astro SDK
from astro import sql as aql
from astro.sql.table import Table

# -------------------- #
# Local module imports #
# -------------------- #
from include.logic import df_cleanup_1 as dfc
from include.logic import core_filter_1 as cf1
from include.logic import core_filter_2 as cf2
from include.logic import goals_or_not as gon
from include.logic import over_under_goals as oug
from include.logic import case_when_logic as cwl

from include.global_variables import global_variables as gv



# from include.logic import apply_filtering_logic, won_last_5_matches


def lenzi(df):
    """Function to check for empty dataframe
    https://stackoverflow.com/questions/19828822/how-do-i-check-if-a-pandas-dataframe-is-empty
    """
    return len(df.index) == 0

# creating a dataframe to show if no fixtures obey filtering conditions
default_df = pd.DataFrame(columns=['Date', 'HomeTeam', 'HomeScore', 'AwayScore', 'AwayTeam'])

row_data = {
    'Date': 'no',
    'HomeTeam': 'fixtures',
    'HomeScore': 'satisfies',
    'AwayScore': 'condition',
    'AwayTeam': ' yet'
}
default_df = default_df.append(row_data, ignore_index=True)


# ----------------- #
# Astro SDK Queries #
# ----------------- #

@aql.dataframe(pool="duckdb")
def find_fixtures(in_table: pd.DataFrame):
    gv.task_log.info(in_table)

    df = in_table
    
    # df = dfc.df_cleanup_1(df)
    # # gv.task_log.info(f"{df}")
    # df = cf1.core_filter_1_optimised(df)
    # # gv.task_log.info(f"{df}")
    # output_df = cf2.core_filter_2_optimised(df)
    # # output_df = apply_filtering_logic(df)

    # Apply the functions using pipe for method chaining
    output_df = (df
               .pipe(dfc.df_cleanup_1)
               .pipe(cf1.core_filter_1)
               .pipe(cf2.core_filter_2)
               .pipe(gon.both_teams_scored_or_not)
               .pipe(oug.add_draw_columns)
               .pipe(oug.add_over_columns)
               .pipe(oug.add_under_columns)
               .pipe(oug.add_under_columns)
               .pipe(cwl.apply_case_when_logic))
    
    gv.task_log.info(output_df)
    if lenzi(output_df) == True:
        gv.task_log.info("df is empty")
        return default_df

# Connect to DuckDB

    conn = duckdb.connect(gv.DB)
    
    try:

        # Register the DataFrame as a temporary table
        conn.register('temp_df', output_df)

        # gv.task_log.info(conn.sql("SELECT 42 AS x").show())
        
        conn.sql(
            f"""DROP TABLE IF EXISTS {gv.REPORTING_TABLE_NAME};"""
        )
        # Create the table if it doesn't exist
        conn.sql(f"""
            CREATE TABLE IF NOT EXISTS {gv.REPORTING_TABLE_NAME} AS 
            SELECT * FROM temp_df;
        """)
        
        # Insert the data
        conn.sql(f"INSERT INTO {gv.REPORTING_TABLE_NAME} SELECT * FROM temp_df")

        # gv.task_log.info(conn.sql("SELECT * from temp_df").show())

        # gv.task_log.info(conn.sql(f"SELECT * from {gv.REPORTING_TABLE_NAME}").show())
        
        conn.commit()
        gv.task_log.info(f"Data inserted into {gv.REPORTING_TABLE_NAME} successfully")
    except Exception as e:
        gv.task_log.error(f"Error occurred: {str(e)}")
        raise
    finally:
        conn.close()

    return None  # or return some status indicator

# @aql.dataframe(pool="duckdb")
# def find_fixtures_c2(in_table: pd.DataFrame):
#     gv.task_log.info(in_table)

#     df = in_table

#     output_df = won_last_5_matches(df)
    
#     gv.task_log.info(output_df)
#     if lenzi(output_df) == True:
#         gv.task_log.info("df is empty")
#         return default_df

#     return output_df


# --- #
# DAG #
# --- #


@dag(
    start_date=datetime(2024, 1, 1),
    schedule=[gv.DS_DUCKDB_IN_FIXTURES],
    catchup=False,
    default_args=gv.default_args,
    description="Runs transformations on fixtures data in DuckDB.",
    tags=["transformation"],
)
def e_transform_fixtures():

    find_fixtures(in_table=Table(
            name=gv.FIXTURES_IN_TABLE_NAME, conn_id=gv.CONN_ID_DUCKDB
        ))

    # find_fixtures(
    #     in_table=Table(
    #         name=gv.FIXTURES_IN_TABLE_NAME, conn_id=gv.CONN_ID_DUCKDB
    #     ),
    #     output_table=Table(
    #         name=gv.REPORTING_TABLE_NAME, conn_id=gv.CONN_ID_DUCKDB
    #     ),
    # )

    # find_fixtures_c2(
    #     in_table=Table(
    #         name=gv.FIXTURES_IN_TABLE_NAME, conn_id=gv.CONN_ID_DUCKDB
    #     ),
    #     output_table=Table(
    #         name=gv.REPORTING_TABLE_NAME_2, conn_id=gv.CONN_ID_DUCKDB
    #     ),
    # )


e_transform_fixtures()
