#
# TEST COMMANDS
#

test-back:
	pep8 ./src/django --max-line-length=120 --exclude='./src/django/VLE/migrations','./src/django/VLE/settings*'
	bash -c 'source ./venv/bin/activate && flake8 --max-line-length=120 src/django --exclude="src/django/VLE/migrations/*","src/django/VLE/settings/*","src/django/VLE/settings.py" && deactivate'
	bash -c "source ./venv/bin/activate && cd ./src/django/ && python3.6 manage.py test && deactivate"

test-front:
	npm run lint --prefix ./src/vue
	npm run test --prefix ./src/vue

test: test-back test-front

#
# DATABSE COMMANDS
#

fill-db: migrate-back
	bash -c 'source ./venv/bin/activate && cd ./src/django && echo "delete from sqlite_sequence where name like \"VLE_%\";" | sqlite3 VLE.db && python3.6 manage.py flush --no-input && python3.6 manage.py preset_db && deactivate'

migrate-back:
	bash -c "source ./venv/bin/activate && cd ./src/django && (rm VLE.db || echo "0") && python3.6 manage.py makemigrations VLE && python3.6 manage.py migrate && deactivate"

#
# DEVELOP COMMANDS
#

run-front:
	bash -c "source ./venv/bin/activate && npm run dev --prefix ./src/vue && deactivate"

run-back:
	bash -c "source ./venv/bin/activate && python3.6 ./src/django/manage.py runserver && deactivate"

setup:
	@echo "This operation will clean old files, press enter to continue (ctrl+c to cancel)"
	@read -r a
	make setup-no-input

setup-no-input:
	@make clean
	# Install apt dependencies and ppa's.
	(sudo apt-cache show python3.6 | grep "Package: python3.6") || \
	(sudo add-apt-repository ppa:deadsnakes/ppa -y; sudo apt update) || echo "0"
	sudo apt install npm nodejs git-flow python3.6 python3-pip pep8 sqlite3 -y
	sudo pip3 install virtualenv

	make reset

	@echo "DONE!"

reset:
	@echo "This operation will clean old files, press enter to continue (ctrl+c to cancel)"
	@read -r a
	@make clean

	# Reinstall venv packages
	virtualenv -p python3.6 venv
	bash -c '\
		source ./venv/bin/activate && \
		pip install git+https://github.com/joestump/python-oauth2.git && \
		pip install -r requirements.txt'

	# Reinstall nodejs dependencies.
	npm install --prefix ./src/vue

	# Remake the database
	make fill-db

	@echo "DONE!"

#
# DEPLOY COMMANDS
#

install:
build:
deploy:
	# TODO: install build deploy
	echo "Not implemented yet"
	# mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
	# bash -c 'bash $(mkfile_path)/deploy/build.sh $(mkfile_path)'

#
# MAKEFILE COMMANDS
#

default:
	make setup
	make test

clean:
	rm -rf ./venv
	rm -rf ./src/vue/node_modules
	rm -rf ./src/django/VLE/migrations
	rm -rf ./src/django/VLE.db

#
# EXTRA COMMANDS
#

superuser:
	bash -c 'source ./venv/bin/activate && python3.6 src/django/manage.py createsuperuser && deactivate'

fix-npm:
	npm cache clean -f
	npm config set strict-ssl false
	sudo npm install -g n
	npm config set strict-ssl true
	sudo n stable

fix-live-reload: SHELL:=/bin/bash
fix-live-reload:
	@bash -c '\
		echo $$(( `sudo cat /proc/sys/fs/inotify/max_user_watches` * 2 )) | \
		sudo tee /proc/sys/fs/inotify/max_user_watches'
