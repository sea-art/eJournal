#!/bin/bash

source settings/deploy.conf
source settings/secrets.conf
source settings/database.conf

sudo a2ensite ejournal.conf || sudo a2ensite ejournal

# Initialize
if [[ $? -ne 0 ]]; then
    rm -rd ./build

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

    # Set apache2 settings
    echo "WSGIPythonHome ${TARGET}/venv
WSGIPythonPath ${TARGET}/django/VLE" > "${APACHEDIR}/conf-available/wsgi.conf"
    sudo a2enconf wsgi

    echo "<VirtualHost *:${PORT}>

    Alias ${HOOKPOINT}index.html ${TARGET}/index.html
    Alias ${HOOKPOINT}static/ ${TARGET}/static/

    <Directory ${TARGET}/static>
        Require all granted
    </Directory>
    <Directory ${TARGET}/django/VLE>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIScriptAlias ${HOOKPOINT} ${TARGET}/django/VLE/wsgi.py

</VirtualHost>" > "${APACHEDIR}/sites-available/ejournal.conf"
    sudo a2ensite ejournal.conf || sudo a2ensite ejournal
    cat ${APACHEDIR}/ports.conf | grep "Listen ${PORT}"
    if [[ $? -ne 0 ]]; then
        echo "Listen ${PORT}" >> ${APACHEDIR}/ports.conf
    fi

    # Create database
fi

# Build vue
npm run-script build --prefix ./src/vue

# Deploy
rsync -a ./venv ${TARGET}
rsync -a --exclude='VLE.db' --exclude='settings/development.py' --exclude='test/' --exclude="*__pycache__" --exclude="migrations/" ./src/django ${TARGET}
rsync -a ./src/vue/dist/ ${TARGET}

sudo sed -i "s@{{DIR}}@${TARGET}/django@g" ${TARGET}/django/VLE/wsgi.py
sudo sed -i "s@http://localhost:8000/@${URL}:${PORT}${HOOKPOINT}@g" ${TARGET}/static/js/*

sudo sed -i "s@{{DATABASE_TYPE}}@${DATABASE_TYPE}@g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s@{{DATABASE_URL}}@${DATABASE_URL}@g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s@{{DATABASE_USER}}@${DATABASE_USER}@g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s@{{DATABASE_PASSWORD}}@${DATABASE_PASSWORD}@g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s@{{DATABASE_PORT}}@${DATABASE_PORT}@g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s@{{DATABASE_HOST}}@${DATABASE_HOST}@g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s@{{BASELINK}}@${URL}:${PORT}${HOOKPOINT}@g" ${TARGET}/django/VLE/settings/production.py

sudo sed -i "s@{{SECRET_KEY}}@${SECRET_KEY}@g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s@{{LTI_SECRET}}@${LTI_SECRET}@g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s@{{LTI_KEY}}@${LTI_KEY}@g" ${TARGET}/django/VLE/settings/production.py

sudo sed -i "s@development@production@g" ${TARGET}/django/manage.py

source ${TARGET}/venv/bin/activate
python ${TARGET}/django/manage.py makemigrations
python ${TARGET}/django/manage.py migrate
deactivate

sudo /etc/init.d/apache2 restart
