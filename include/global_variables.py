from airflow import Dataset
import logging
import os
from minio import Minio
from pendulum import duration
import json

DS_START = Dataset("start")

# MinIO connection config
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_IP = "host.docker.internal:9000"
# WEATHER_BUCKET_NAME = "weather"
FIXTURES_BUCKET_NAME = "fixtures"
ARCHIVE_BUCKET_NAME = "archive"

# DAG default arguments
default_args = {
    "owner": "Edun Joshua",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": duration(minutes=5),
}

LEAGUE_IDS=[20,21]

# Source file path fixtures data
TEMP_GLOBAL_PATH = f"{os.environ['AIRFLOW_HOME']}/include/fixtures/temp_global.csv"

# Datasets
DS_FIXTURES_DATA_MINIO = Dataset(f"minio://{FIXTURES_BUCKET_NAME}")
# DS_WEATHER_DATA_MINIO = Dataset(f"minio://{WEATHER_BUCKET_NAME}")
# DS_DUCKDB_IN_WEATHER = Dataset("duckdb://in_weather")
DS_DUCKDB_IN_FIXTURES = Dataset("duckdb://in_fixtures")
DS_DUCKDB_REPORTING = Dataset("duckdb://reporting")
DS_START = Dataset("start")

# utility functions
def get_minio_client():
    client = Minio(MINIO_IP, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, secure=False)

    return client

# get Airflow task logger
task_log = logging.getLogger("airflow.task")