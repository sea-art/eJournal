#!/bin/bash

source settings/deploy.conf
source settings/secrets.conf
source settings/database.conf

sudo /etc/init.d/apache2 stop

sudo echo "WSGIPythonHome ${TARGET}/venv
WSGIPythonPath ${TARGET}/django/VLE" > "${APACHE_DIR}/conf-available/wsgi.conf"
    sudo a2enconf wsgi

sudo echo "
<VirtualHost *:${PORT}>
    Alias ${HOOKPOINT}index.html '${TARGET}index.html'
    Alias ${HOOKPOINT}static/ '${TARGET}static/'
    ServerName www.${SERVERNAME}
    ServerAlias ${SERVERNAME}

    <Directory ${TARGET}static>
        Require all granted
    </Directory>
</VirtualHost>
" > "${APACHE_DIR}/sites-available/ejournal.conf"
sudo echo "
<VirtualHost *:${PORT}>
    ServerName www.${APIURL}
    ServerAlias ${APIURL}

    <Directory ${TARGET}django/static>
        Require all granted
    </Directory>
    <Directory ${TARGET}django/VLE>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIScriptAlias ${HOOKPOINT} ${TARGET}django/VLE/wsgi.py
</VirtualHost>
" > "${APACHE_DIR}/sites-available/ejournalapi.conf"

sudo a2ensite ejournal.conf || sudo a2ensite ejournal
sudo a2ensite ejournalapi.conf || sudo a2ensite ejournalapi
cat ${APACHE_DIR}/ports.conf | grep -w "Listen ${PORT}"
if [[ $? -ne 0 ]]; then
    sudo echo "Listen ${PORT}" >> ${APACHE_DIR}/ports.conf
fi

sudo /etc/init.d/apache2 start
