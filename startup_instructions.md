*View Fixtures on Port 8501*

1. Go to port 8501 to view fixtures.
    - If port is active, ignore the following instructions.
    - If port is INACTIVE, follow these steps:

*Activate Port*

1. Run the following commands in the terminal in order:
    - `curl -sSL (link unavailable) | sudo bash -s -- v1.28.0`
    - `sudo chmod -R 777 include/`
2. Start or restart Astro:
    -  `astro dev start`
    - If already started: `astro dev restart`

*Access DAGs*

1. Go to port 8080.
2. If prompted, log in with username and password: "admin".
3. Toggle all DAGs (active DAGs have a blue background).
4. Trigger the "start DAG" by:
    - Going to the "Action" column under the "a_start" DAG.
    - Clicking the "..." button.
    - Selecting "Trigger DAG".

*Verify Fixtures*

1. Wait 10 minutes or longer.
2. View port 8501 to see fixtures