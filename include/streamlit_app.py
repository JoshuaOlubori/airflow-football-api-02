# --------------- #
# PACKAGE IMPORTS #
# --------------- #

import streamlit as st
import duckdb
import pandas as pd
from datetime import date, datetime
import altair as alt
# from include.global_variables import global_variables as gv




duck_db_instance_path = (
    "/app/include/dwh"  # when changing this value also change the db name in .env
)

APP_USER = "Mr. Akindele"
# -------------- #
# DuckDB Queries #
# -------------- #


def list_currently_available_tables(db=duck_db_instance_path):
    cursor = duckdb.connect(db)
    tables = cursor.execute("SHOW TABLES;").fetchall()
    cursor.close()
    return [table[0] for table in tables]








def get_fixtures(db=duck_db_instance_path):

    cursor = duckdb.connect(db)
    fixtures_data = cursor.execute(
        f"""SELECT * FROM reporting_table ORDER BY league_name, date DESC;"""
    ).fetchall()

    fixtures_data_col_names = cursor.execute(
        f"""SELECT column_name from information_schema.columns where table_name = 'reporting_table';"""
    ).fetchall()

    df = pd.DataFrame(
        fixtures_data, columns=[x[0] for x in fixtures_data_col_names]
    )
    cursor.close()

    return df


# def get_fixtures_2(db=duck_db_instance_path):

#     cursor = duckdb.connect(db)
#     fixtures_data = cursor.execute(
#         f"""SELECT * FROM reporting_table_2;"""
#     ).fetchall()

#     fixtures_data_col_names = cursor.execute(
#         f"""SELECT column_name from information_schema.columns where table_name = 'reporting_table_2';"""
#     ).fetchall()

#     df = pd.DataFrame(
#         fixtures_data, columns=[x[0] for x in fixtures_data_col_names]
#     )
#     cursor.close()

#     return df




# ------------ #
# Query DuckDB #
# ------------ #


tables = list_currently_available_tables()


if "reporting_table" in tables:
    fixtures_result_table = get_fixtures()


# if "reporting_table_2" in tables:
#     fixtures_result_table_2 = get_fixtures_2()



# ------------- #
# STREAMLIT APP #
# ------------- #

st.title("Fixtures Transformation Results")



st.markdown(f"Hello {APP_USER} :wave: Welcome to your Streamlit App! :blush:")
# Get the DataFrame
# Filter options
st.sidebar.header("Filter Options")

# Create selectboxes for filtering criteria
filter_won_3_games_or_more = st.sidebar.selectbox(
    "Teams that won 3 or more games against common opponents in their last 5 games, in the current season:",
    options=["All", "T", "F"],
    index=0  # Default to "All"
)


filter_team_won_all_last_5_games = st.sidebar.selectbox(
    "Teams that won all last 5 games (In addition to the above filter):",
    options=["All", "T", "F"],
    index=0  # Default to "All"
)

# Apply filters
filtered_df = fixtures_result_table
if filter_won_3_games_or_more != "All":
    filtered_df = filtered_df[filtered_df["won_3_games_or_more"] == filter_won_3_games_or_more]
if filter_team_won_all_last_5_games != "All":
    filtered_df = filtered_df[filtered_df["team_won_all_last_5_games"] == filter_team_won_all_last_5_games]

# Display the filtered DataFrame
with st.expander("All fixtures"):
    st.dataframe(filtered_df)