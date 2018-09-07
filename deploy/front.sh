#!/bin/bash

source settings/deploy.conf
source settings/secrets.conf
source settings/database.conf

# Build vue
sudo npm run-script build --prefix ./src/vue

# Deploy
sudo rsync -a ./src/vue/dist/ ${TARGET}
sudo sed -i "s@http://localhost:8000/@${TYPE}://${APIURL}${HOOKPOINT}@g" ${TARGET}/static/js/*
