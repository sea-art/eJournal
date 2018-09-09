#!/bin/bash

source settings/deploy.conf
source settings/secrets.conf
source settings/database.conf

sudo /etc/init.d/apache2 stop

echo "WSGIPythonHome ${TARGET}/venv
WSGIPythonPath ${TARGET}/django/VLE
WSGIPassAuthorization On" | sudo tee "${APACHE_DIR}/conf-available/ejournalwsgi.conf"

sudo a2enmod rewrite
sudo a2enmod wsgi
sudo a2enconf ejournalwsgi

echo "
<VirtualHost *:${PORT}>
    Alias ${HOOKPOINT} '${TARGET}'
    ServerName www.${SERVERNAME}
    ServerAlias ${SERVERNAME}

    <Directory ${TARGET}/static>
        Require all granted
    </Directory>

    <Directory ${TARGET}>
        Options -Indexes
        <IfModule mod_rewrite.c>
            RewriteEngine On
            RewriteBase ${HOOKPOINT}
            RewriteRule ^index\.html$ - [L]
            RewriteCond %{REQUEST_FILENAME} !-f
            RewriteCond %{REQUEST_FILENAME} !-d
            RewriteRule . ${TARGET}/index.html [L]
        </IfModule>
    </Directory>

    <Directory ${TARGET}/django/>
        Deny from all
    </Directory>

    <Directory ${TARGET}/venv/>
        Deny from all
    </Directory>
</VirtualHost>
" | sudo tee "${APACHE_DIR}/sites-available/ejournal.conf"
echo "
<VirtualHost *:${PORT}>
    ServerName www.${APIURL}
    ServerAlias ${APIURL}

    <Directory ${TARGET}/django/static>
        Require all granted
    </Directory>
    <Directory ${TARGET}/django/VLE>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIScriptAlias ${HOOKPOINT} ${TARGET}/django/VLE/wsgi.py
</VirtualHost>
" | sudo tee "${APACHE_DIR}/sites-available/ejournalapi.conf"

sudo a2ensite ejournal.conf || sudo a2ensite ejournal
sudo a2ensite ejournalapi.conf || sudo a2ensite ejournalapi
cat ${APACHE_DIR}/ports.conf | grep -w "Listen ${PORT}"
if [[ $? -ne 0 ]]; then
    sudo echo "Listen ${PORT}" >> ${APACHE_DIR}/ports.conf
fi

sudo /etc/init.d/apache2 start
sudo systemctl reload apache2
