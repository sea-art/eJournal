import os

key_path = 'awskey.pem'
user = 'ubuntu'
dest = 'ec2-34-207-89-78.compute-1.amazonaws.com'
src = 'ec2-54-197-42-74.compute-1.amazonaws.com'
# src_path = 'backups'
# dest_path = 'backups'
dest_path = 'backups'
src_path = '/webapps/ejournal/media'
reverted_bool = False
changed_commit = ""


# Sync application back-up folder from remote and commit remote folder
def rsync_pull():
    os.system(
        f'rsync --exclude .git/ --exclude .gitignore -az -P --delete -e "ssh -ax -i {key_path}" {user}@{dest}:{src_path}/ {dest_path}')
    os.system(f'cd {dest_path} ; git init ; git add . ; git commit -m "_" ')


if __name__ == '__main__':
    rsync_pull()
