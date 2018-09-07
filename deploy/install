#!/bin/bash
path=$1
source settings/deploy.conf

# Install apache and wsgi
sudo apt -y install apache2 apache2-dev libapache2-mod-wsgi libpq-dev postgresql postgresql-contrib
wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.6.4.tar.gz -P build
tar xfz build/4.6.4.tar.gz -C build

source ${path}/venv/bin/activate
    cd ${path}/build/mod_wsgi-4.6.4
    ${path}/configure
deactivate

make
sudo make install
cd ${path}


sudo rsync -a ${path}/venv ${TARGET}
source ${TARGET}venv/bin/activate
    pip install -r requirements.txt
deactivate
