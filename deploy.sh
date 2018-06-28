#!/bin/bash
type=$1

chmod +x deploy*.sh
echo $type
if [[ $type == "init" ]]; then
    ./deploy_init.sh
fi

if [[ $type == "apache" || $type == "init" ]]; then
    sudo ./deploy_apache.sh
fi

if [[ $type == "db" || $type == "init" ]]; then
    ./deploy_db.sh
fi

if [[ $type == "back" || $type == "init" ]]; then
    ./deploy_back.sh
fi

if [[ $type == "front" || $type == "init" ]]; then
    ./deploy_front.sh
fi
