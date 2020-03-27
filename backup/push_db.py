import os

key_path = '{{ key-placeholder }}'
user = '{{ user-placeholder }} '
application_server = '{{ application-server-placeholder }}'
backup_server = '{{ backup-server-placeholder }}'
backup_server_path = 'backups-db'
application_server_path = '/backup'
reverted_bool = False
changed_commit = ""


# Sync application back-up folder to remote and commit remote folder
def rsync_push():
    os.system(
        f'rsync --exclude .git/ --exclude .gitignore -az -P --delete -e "ssh -ax -i {key_path}" {application_server_path}/ {user}@{backup_server}:{backup_server_path}')
    os.system(f'ssh {user}@{backup_server} -i {key_path} "cd {backup_server_path} ; git add . ; git commit -m "_""')


if __name__ == '__main__':
    rsync_push()
