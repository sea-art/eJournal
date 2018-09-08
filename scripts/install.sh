#!/bin/bash
path=$1
source ${path}/settings/deploy.conf
source ${path}/settings/database.conf

# Install apache and wsgi
sudo apt-get -y install apache2 apache2-dev libapache2-mod-wsgi libpq-dev postgresql postgresql-contrib
wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.6.4.tar.gz -P ${path}/build
tar xfz ${path}/build/4.6.4.tar.gz -C build

# Configure mod wsgi
source ${path}/venv/bin/activate
    cd ${path}/build/mod_wsgi-4.6.4
    ./configure --with-python=${path}/venv/bin/python
deactivate

# Install mod wsgi
make
sudo make install
cd ${path}

# Sync venv (with the installed packages) to the target directory
sudo rsync -a ${path}/venv ${TARGET}
source ${TARGET}/venv/bin/activate
    pip install -r requirements.txt
deactivate

# Install postgres
source ${TARGET}/venv/bin/activate
    pip install psycopg2-binary
deactivate

# Create postgres user
sudo -u postgres -i bash << EOF
echo "CREATE USER ${DATABASE_USER} LOGIN PASSWORD '${DATABASE_PASSWORD}';" | psql
echo "CREATE DATABASE ${DATABASE_NAME} WITH OWNER = ${DATABASE_USER};" | psql
echo "ALTER USER ${DATABASE_USER} WITH PASSWORD '${DATABASE_PASSWORD}';" | psql
echo "GRANT ALL PRIVILEGES ON DATABASE ${DATABASE_NAME} TO ${DATABASE_USER};" | psql
EOF
