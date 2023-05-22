#!/usr/bin/env bash
set -x
set -eo pipefail
# Check Dependencies
if ! [ -x "$(command -v psql)" ]; then
    echo >&2 "Error: psql is not installed."
    exit 1
fi
# TODO update with alembic
if ! [ -x "$(command -v alembic)" ]; then
    echo >&2 "Error: alembic is not installed."
    echo >&2 "Use:"
    # TODO update with alembic
    echo >&2 "   pip install alembic"
    echo >&2 "to install it."
    exit 1
fi
# Check if a custom user has been set, otherwise default
# to 'postgres'
DB_USER="${POSTGRES_USER:=postgres}"
# Check if a custom password has been set, otherwise default
# to 'password'
DB_PASSWORD="${POSTGRES_PASSWORDs:=password}"
# Check if a custom database name has been set, otherwise
# default to 'newsletter'
DB_NAME="${POSTGRES_DB:=nostar}"
# Check if a custom post has been set otherwise,
# default to 5430
DB_PORT="${POSTGRES_PORT:=5430}"
# Check if a custom host has been set otherwise,
# default to localhost
DB_HOST="${POSTGRES_HOST:=localhost}"
# Launch Postgres using Docker...
# Allow to skip Docker if a dockerized Postgres
# DB is already running
if [[ -z "${SKIP_DOCKER}" ]]
then
    docker run \
        -e POSTGRES_USER=${DB_USER} \
        -e POSTGRES_PASSWORD=${DB_PASSWORD} \
        -e POSTGRES_DB=${DB_NAME} \
        -p "${DB_PORT}":5432 \
        -d postgres \
        postgres -N 1000
    #               ^ Increase max # connections for testing purposes
fi
# Keep pinging Postgres until it is ready to accept connections
export PGPASSWORD="${DB_PASSWORD}"
until psql -h "${DB_HOST}" -U "${DB_USER}" -p "${DB_PORT}" -d "postgres" -c '\q'; do
    >&2 echo "Postgres is still unavailable - Sleeping..."
    sleep 1
done
# Ready
>&2 echo "Postgres is up and running on port ${DB_PORT}..."

# Create - TODO ensure that the proper permissions are established
psql -h "${DB_HOST}" -U "${DB_USER}" -p "${DB_PORT}" -tc "SELECT 1 FROM pg_database WHERE datname = '${DB_NAME}'" | \
    grep -q 1 || \
    psql -U "${DB_USER}" -p "${DB_PORT}" -c "CREATE DATABASE '${DB_NAME}'"
# Run Migrations
alembic upgrade head # TODO check that this is the right alembic command to use
>&2 echo "Postgres has been migrated... Ready to go."
