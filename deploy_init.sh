#!/bin/bash

source settings/deploy.conf
source settings/secrets.conf
source settings/database.conf

sudo rm -rd ./build
sudo rm -rd ${TARGET}

# Install apache and wsgi
sudo apt -y install apache2 apache2-dev libapache2-mod-wsgi libpq-dev postgresql postgresql-contrib
wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.6.4.tar.gz -P build
tar xfz build/4.6.4.tar.gz -C build

source ./venv/bin/activate
cd ./build/mod_wsgi-4.6.4
./configure
deactivate

make
sudo make install
cd ../../

sudo rsync -a ./venv ${TARGET}
source ${TARGET}venv/bin/activate
pip install -r requirements.txt
deactivate
