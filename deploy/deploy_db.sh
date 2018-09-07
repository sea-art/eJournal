#!/bin/bash

source settings/deploy.conf
source settings/secrets.conf
source settings/database.conf

source ${TARGET}venv/bin/activate
pip install psycopg2-binary
deactivate

sudo -u postgres -i bash << EOF
echo "CREATE USER ${DATABASE_USER} LOGIN PASSWORD '${DATABASE_PASSWORD}';" | psql
echo "CREATE DATABASE ${DATABASE_NAME} WITH OWNER = ${DATABASE_USER};" | psql
echo "ALTER USER ${DATABASE_USER} WITH PASSWORD '${DATABASE_PASSWORD}';" | psql
echo "GRANT ALL PRIVILEGES ON DATABASE ${DATABASE_NAME} TO ${DATABASE_USER};" | psql
EOF
