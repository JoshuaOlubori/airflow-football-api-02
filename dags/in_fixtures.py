"""DAG that loads climate ingests from local csv files into MinIO."""
from airflow.decorators import dag
from pendulum import datetime
import io

from include.global_variables import global_variables as gv
from include.custom_task_groups.create_bucket import CreateBucket
from include.custom_operators.minio import LocalFilesystemToMinIOOperator

def in_fixtures_data():

    # create an instance of the CreateBucket task group consisting of 5 tasks
    create_bucket_tg = CreateBucket(
        task_id="create_fixtures_bucket", bucket_name=gv.FIXTURES_BUCKET_NAME
    )

    # use the custom LocalCSVToMinIOOperator to read the contents in /include/fixtures
    # into MinIO. This task uses dynamic task allowing you to add additional files to
    # the folder and reading them in without changing any DAG code
    ingest_fixtures_data = LocalFilesystemToMinIOOperator.partial(
        task_id="ingest_fixtures_data",
        bucket_name=gv.FIXTURES_BUCKET_NAME,
        outlets=[gv.DS_FIXTURES_DATA_MINIO],
    ).expand_kwargs(
        [
            {
                "local_file_path": gv.TEMP_GLOBAL_PATH,
                "object_name": gv.TEMP_GLOBAL_PATH.split("/")[-1],
            },
        ]
    )

    # set dependencies
    create_bucket_tg >> ingest_fixtures_data


in_fixtures_data()
