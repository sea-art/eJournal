import os

key_path = '{{ key-placeholder }}'
user = '{{ user-placeholder }} '
application_server = '{{ application-server-placeholder }}'
backup_server = '{{ backup-server-placeholder }}'
backup_server_path = 'backups'
application_server_path = 'backups'
reverted_bool = False
changed_commit = ""


# makes backup folder on remote and git init
def init_remote():
    os.system(f'ssh {user}@{backup_server} -i {key_path} "mkdir {backup_server_path}-media ; cd {backup_server_path}-media ; git init"')
    os.system(f'ssh {user}@{backup_server} -i {key_path} "mkdir {backup_server_path}-db ; cd {backup_server_path}-db ; git init"')


if __name__ == '__main__':
    init_remote()
