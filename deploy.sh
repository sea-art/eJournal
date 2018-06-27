#!/bin/bash

source settings/deploy.conf
sudo a2ensite ejournal.conf || sudo a2ensite ejournal

# Initialize
if [[ $? -ne 0 ]]; then
    rm -rd ./build

    # Install apache and wsgi
    sudo apt -y install apache2 apache2-dev libapache2-mod-wsgi
    wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.6.4.tar.gz -P build
    tar xfz build/4.6.4.tar.gz -C build

    source ./venv/bin/activate
    cd ./build/mod_wsgi-4.6.4
    ./configure
    deactivate

    make
    sudo make install

    cd ../../

    # Set apache2 settings
    echo "WSGIPythonHome ${TARGET}/venv
WSGIPythonPath ${TARGET}/django/VLE" > "${APACHEDIR}/conf-available/wsgi.conf"
    sudo a2enconf wsgi
    echo "<VirtualHost *:${PORT}>
    WSGIScriptAlias ${HOOKPOINT} ${TARGET}/django/VLE/wsgi.py
    <Directory ${TARGET}/django/VLE>
    <Files wsgi.py>
    Require all granted
    </Files>
    </Directory>
</VirtualHost>" > "${APACHEDIR}/sites-available/ejournal.conf"
    sudo a2ensite ejournal.conf || sudo a2ensite ejournal
fi

# Deploy
rsync -a ./venv ${TARGET}
rsync -a --exclude='settings.py' --exclude='VLE.db' --exclude='test/' --exclude="*__pycache__" --exclude="migrations/" ./src/django ${TARGET}
