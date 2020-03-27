import os

key_path = 'awskey.pem'
user = 'ubuntu'
dest = 'ec2-34-207-89-78.compute-1.amazonaws.com'
src = 'ec2-54-197-42-74.compute-1.amazonaws.com'
src_path = 'backups-db'
dest_path = '/backup'
reverted_bool = False
changed_commit = ""


# Sync application back-up folder to remote and commit remote folder
def rsync_push():
    os.system(
        f'rsync --exclude .git/ --exclude .gitignore -az -P --delete -e "ssh -ax -i {key_path}" {dest_path}/ {user}@{src}:{src_path}')
    os.system(f'ssh {user}@{src} -i {key_path} "cd {src_path} ; git add . ; git commit -m "_""')


if __name__ == '__main__':
    rsync_push()
