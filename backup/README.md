<p align="center">
    <img width="250" src="https://avatars1.githubusercontent.com/u/41028230"/>
</p>

[![Build Status](https://travis-ci.com/eJourn-al/eJournal.svg?branch=develop)](https://travis-ci.com/eJourn-al/eJournal) [![Coverage Status](https://codecov.io/gh/eJourn-al/eJournal/branch/develop/graph/badge.svg)](https://codecov.io/gh/eJourn-al/eJournal)

This part of the application ensures that the backups end up on the backup server, and that backups can be restored neatly. 

## Configurating the servers

`ansible-playbook -i hosts playbook.yml`

Installs all dependensies and places the files on the right location on the remote servers. 

## Initialize repository

`Python3 init_repo.py`

Initializes the repository on the backup server

## Push

`Python3 push.py`

Takes the Media backups from the application server and sends them to the backup server.

## Push_db

`Python3 push_db.py`

Takes the Postgres Database backups from the application server and sends them to the backup server.

## Pull

`Python3 pull.py`

Pulls both the postgres and media backups from the application server to the backup server.

## Pull

`Python3 pull.py`

Pulls both the postgres and media backups from the application server to the backup server.

## Recover media backup

`Python3 recover_backup.py`

Retrieves the backup from the backup-server to the application server and restores it. The user can choose which files he wants to restore. To restore an older backup, you can go back to an older commit. 

## Recover database backup

`Python3 recover_backup_db.py`

Same as recover media backup, but for postgres backup.

Together with:

Jeroen van Bennekum, Xavier van Dommelen, Okke van Eck, Hendrik Huang, Siard Keulen, Joey Lai, Teun Mathijssen, Mohammed el Mochoui, Rick Watertor, Dennis Wind, Zi Long Zhu.

## Contributing

For information about contributing to the project, see [CONTRIBUTING.MD](CONTRIBUTING.MD).
