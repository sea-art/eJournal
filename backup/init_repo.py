import os

key_path = 'awskey.pem'
user = 'ubuntu'
dest = 'ec2-34-207-89-78.compute-1.amazonaws.com'
src = 'ec2-54-197-42-74.compute-1.amazonaws.com'
src_path = 'backups'
dest_path = 'backups'
reverted_bool = False
changed_commit = ""


# makes backup folder on remote and git init
def init_remote():
    os.system(f'ssh {user}@{src} -i {key_path} "mkdir {src_path}-media ; cd {src_path}-media ; git init"')
    os.system(f'ssh {user}@{src} -i {key_path} "mkdir {src_path}-db ; cd {src_path}-db ; git init"')


if __name__ == '__main__':
    init_remote()
