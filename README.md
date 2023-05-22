# nostar-scrape

## Prerequisites
(1) Docker
(2) psql for Postgres
(3) alembic for programmatic DB maintenance
(4) python

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