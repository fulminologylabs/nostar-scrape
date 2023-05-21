#!/usr/bin/env bash
set -x
set -eo pipefail
# Check Dependencies
if ! [ -x "$(command -v psql)" ]; then
    echo >&2 "Error: psql is not installed."
    exit 1
fi
# TODO update with alembic
if ! [ -x "$(command -v sqlx)" ]; then
    echo >&2 "Error: sqlx is not installed."
    echo >&2 "Use:"
    # TODO update with alembic
    echo >&2 "   cargo install sqlx-cli --no-default-features --features rustls,postgres"
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
# Export URL
DATABASE_URL=postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
export DATABASE_URL
# Create
sqlx database create
# Run Migrations
sqlx migrate run
>&2 echo "Postgres has been migrated... Ready to go."
