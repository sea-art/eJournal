import os

key_path = '{{ key-placeholder }}'
user = '{{ user-placeholder }} '
application_server = '{{ application-server-placeholder }}'
backup_server = '{{ backup-server-placeholder }}'
# backup_server_path = 'backups'
# application_server_path = 'backups'
application_server_path = 'backups'
backup_server_path = '/webapps/ejournal/media'
reverted_bool = False
changed_commit = ""


# Sync application back-up folder from remote and commit remote folder
def rsync_pull():
    os.system(
        f'rsync --exclude .git/ --exclude .gitignore -az -P --delete -e "ssh -ax -i {key_path}" {user}@{application_server}:{backup_server_path}/ {application_server_path}')
    os.system(f'cd {application_server_path} ; git init ; git add . ; git commit -m "_" ')


if __name__ == '__main__':
    rsync_pull()
