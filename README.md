# nostar-scrape

## Prerequisites
- Docker
- psql for Postgres
- alembic for programmatic DB maintenance
- Python (3.10 ideally; 3.7+ should be fine)

# Setup virtual environment
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Set Environment Variables
```
touch .env
```
Then copy/paste the below into `.env`
```
DATABASE_URL="postgres://postgres:password@localhost:5430/nostar"

DB_USER="postgres"
DB_HOST="localhost"
DB_PASSWORD="password"
DB_PORT="5430"
DB_NAME="nostar"
DB_DRIVER="psycopg2"
```

## Start DB
Note, Docker must be running, you must run from virtual environment, and the `.env` must be populated.

Grant execution permission (Mac OS)
```
chmod 755 ./scripts/
```

Start the DB
```
./scripts/init_db.sh
```

To confirm the DB is up in running look for a running Postgres container in Docker, then open its terminal.
Make sure you can access the DB through the Docker terminal with the following
```
psql -h localhost -U postgres -d nostar
```
Confirm that the migrations ran properly... Running
```
\dt
```
Should return you something like
```
 Schema |      Name       | Type  |  Owner   
--------+-----------------+-------+----------
 public | alembic_version | table | postgres
 public | batch           | table | postgres
 public | event_kind      | table | postgres
 public | filter          | table | postgres
 public | job             | table | postgres
 public | job_type        | table | postgres
 public | relay           | table | postgres
 public | relay_config    | table | postgres
 public | subscription    | table | postgres
 public | text_note       | table | postgres
(10 rows)alembic_versionalembic_version
```
## Migrate the DB
Alembic docs: https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment
```
alembic revision -m "< description of my change >"
```
Then, locate the generated file in the `migrations/` directory and populate the upgrade and downgrade
functions.

To apply the change
```
alembic upgrade head
```

To upgrade or downgrade recent revisions
```
alembic downgrade -1
    
alembic upgrade +1
```
## Tests
```
pytest
```

## Clear PyCache
```
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

find . | grep -E "(.pytest_cache|\*)" | xargs rm -rf
```