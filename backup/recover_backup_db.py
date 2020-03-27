import os
import subprocess
from datetime import datetime
import time

"""
- Testen op twee remote servers
- Ansible 
- Cron Job
- Big files 
"""

key_path = 'awskey.pem'
user = 'ubuntu'
dest = 'ec2-34-207-89-78.compute-1.amazonaws.com'
src = 'ec2-54-197-42-74.compute-1.amazonaws.com'
# src_path = 'backups'
# dest_path = 'backups'
src_path = 'backups-db'
dest_path = '/backup'
reverted_bool = False
changed_commit = ""


def ssh_command(cmd):
    ssh = subprocess.Popen(["ssh", "-i", f"{key_path}", f'{user}@{src}', cmd],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    return ssh


# Recovers commit on remote server
def recover_commit():
    # Get all commits on SSH and print them
    cmd = f'cd {src_path} ; git log --all --pretty="format:%h -> %cr"'
    ssh = ssh_command(cmd)
    # tmp = ssh.stdout.read().decode('utf-8')
    tmp = ssh.stdout.read().decode('utf-8')
    commits = tmp.splitlines()

    current_commit = print_current_commit()

    for index, commit in enumerate(commits):
        # Print commits, arrow points to current commit
        arrow = "<---" if current_commit[:-1] == commit[:7] else ""
        print(f'{index}: {commit} {arrow}')
        commits[index] = commit[:7]

    # Let user pick his commit (based on date)
    print(f'Pick your commit by choosing a number between 0 and {len(commits) - 1}:')

    choice = int(input())

    # Make sure choice is in range
    while choice is None or choice > (len(commits) - 1):
        print('That number is not in range, try again!')
        choice = int(input())

    commit = commits[choice]
    # Checkout to commit, revert the backup
    cmd = f'cd {src_path} ; git checkout {commit}'
    ssh = ssh_command(cmd)
    revert_backup()


def new_branch():
    # Start new branch at chosen commit
    branch_name = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    cmd = f'cd {src_path} ; git checkout -b {branch_name}'
    ssh = ssh_command(cmd)


def print_current_commit():
    cmd = f'cd {src_path} ; git rev-parse --short HEAD'
    ssh = ssh_command(cmd)
    tmp = ssh.stdout.read()
    return tmp.decode('utf-8')


def print_current_branch():
    cmd = f'cd {src_path} ; git rev-parse --abbrev-ref HEAD'
    ssh = ssh_command(cmd)
    tmp = ssh.stdout.read()
    return tmp.decode('utf-8')


def checkout_first_branch(branch):
    cmd = f'cd {src_path} ; git checkout {branch}'
    ssh = ssh_command(cmd)
    tmp = ssh.stdout.read()
    return tmp.decode('utf-8')


# Get single back-up from remote
def revert_backup():
    # SSH needs time to refresh
    time.sleep(5)

    # Get files list from SSH and print them
    cmd = f'cd /home/ubuntu ; cd {src_path} ; ls'
    ssh = ssh_command(cmd)
    tmp = ssh.stdout.read()
    files = tmp.decode('utf-8').splitlines()

    print("------------------------")

    for file in files:
        print(f'{file}')

    # Ask user if he wants these files
    print(f'These are the files you are going to pull, press y if you want these.')
    print(f'If you want an older commit, press "x". ')

    choice = input()

    # If yes, pull these files
    if choice == "Y" or choice == 'y':
        os.system(
            f'rsync --exclude .git/ --exclude .gitignore -az -P --delete -e "ssh -ax -i {key_path}" {user}@{src}:{src_path}/ {dest_path}')

        global changed_commit
        changed_commit = print_current_commit()[:-1]

    # If not, recover older commit
    elif isinstance(choice, str):
        if choice == 'x' or choice == 'X':
            recover_commit()


if __name__ == '__main__':
    first = print_current_commit()[:-1]
    first_branch = print_current_branch()
    revert_backup()
    changed_commit = changed_commit
    if not (first == changed_commit):
        new_branch()
    else:
        checkout_first_branch(first_branch)
