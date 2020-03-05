ifdef test
TOTEST=-k ${test}
else
TOTEST=
endif

ifeq (,$(wildcard ./pass.txt))
ansible_use = --ask-vault-pass
else
ansible_use = --vault-password-file pass.txt
endif

postgres_db = ejournal
postgres_test_db = test_$(postgres_db)
postgres_dev_user = ejournal
postgres_dev_user_pass = password

##### TEST COMMANDS #####

test-back:
	pep8 ./src/django --max-line-length=120 --exclude='./src/django/VLE/migrations','./src/django/VLE/settings*'
	bash -c 'source ./venv/bin/activate && flake8 --max-line-length=120 src/django --exclude="src/django/VLE/migrations/*","src/django/VLE/settings/*","src/django/VLE/settings.py","src/django/VLE/tasks/__init__.py" && deactivate'
	bash -c "source ./venv/bin/activate && pytest -n auto --cov=VLE --cov-config .coveragerc src/django/test ${TOTEST} && deactivate"
	bash -c 'source ./venv/bin/activate && isort -rc src/django/ && deactivate'

test-front:
	npm run lint --prefix ./src/vue

display-coverage:
	bash -c "source ./venv/bin/activate && cd src/django/ && coverage report -m && deactivate"

test: test-front test-back

run-test:
	bash -c 'source ./venv/bin/activate && cd ./src/django && python manage.py test test.test_$(arg)'

##### DEVELOP COMMANDS #####

run-front:
	bash -c "source ./venv/bin/activate && npm run serve --prefix ./src/vue && deactivate"

run-back: isort
	bash -c "source ./venv/bin/activate && python ./src/django/manage.py runserver && deactivate"

isort:
	bash -c 'source ./venv/bin/activate && isort -rc src/django/ && deactivate'


setup:
	@echo "This operation will clean old files, press enter to continue (ctrl+c to cancel)"
	@read -r a
	make setup-no-input
setup-no-input:
	@make clean

	# Install apt dependencies and ppa's.
	(sudo apt-cache show python3.6 | grep "Package: python3.6") || \
	(sudo add-apt-repository ppa:deadsnakes/ppa -y; sudo apt update) || echo "0"

	sudo apt install npm -y
	sudo npm install npm@latest -g
	sudo apt install nodejs python3 python3-pip pep8 libpq-dev python3-dev postgresql postgresql-contrib rabbitmq-server python3-setuptools -y

	make setup-venv requirements_file=local.txt

	# Reinstall nodejs dependencies.
	npm ci --prefix ./src/vue

	make preset-db-no-input
	bash -c 'source ./venv/bin/activate && cd ./src/django && python manage.py migrate django_celery_results && deactivate'

	@echo "DONE!"

setup-travis:
	(sudo apt-cache show python3.6 | grep "Package: python3.6") || (sudo add-apt-repository ppa:deadsnakes/ppa -y; sudo apt update) || echo "0"
	sudo apt install npm -y
	sudo apt install nodejs python3 python3-pip pep8 python3-setuptools -y

	sudo pip3 install virtualenv
	virtualenv -p python3 venv
	bash -c 'source ./venv/bin/activate && pip install -r requirements/ci.txt && deactivate'

	# Reinstall nodejs dependencies.
	npm ci --prefix ./src/vue

	@echo "DONE!"

setup-venv:
	sudo pip3 install virtualenv
	virtualenv -p python3 venv
	bash -c '\
		source ./venv/bin/activate && \
		pip install -r requirements/$(requirements_file) && \
		isort -rc src/django/ && \
		ansible-playbook ./system_configuration_tools/provision-local.yml --ask-become-pass --ask-vault-pass && \
		deactivate'

##### DEPLOY COMMANDS ######

ansible-test-connection:
	@bash -c 'source ./venv/bin/activate && ansible -m ping all --ask-become-pass && deactivate'

run-ansible-provision:
	@bash -c 'source ./venv/bin/activate && \
		ansible-playbook ./system_configuration_tools/provision-servers.yml --ask-become-pass ${ansible_use} \
		&& deactivate'

run-ansible-deploy:
	@bash -c 'source ./venv/bin/activate && \
		ansible-playbook ./system_configuration_tools/provision-servers.yml --ask-become-pass --tags "deploy_front,deploy_back" ${ansible_use} \
		&& deactivate'

run-ansible-deploy-front:
	@bash -c 'source ./venv/bin/activate && \
		ansible-playbook ./system_configuration_tools/provision-servers.yml --ask-become-pass --tags "deploy_front" ${ansible_use} \
		&& deactivate'

run-ansible-deploy-back:
	@bash -c 'source ./venv/bin/activate && \
		ansible-playbook ./system_configuration_tools/provision-servers.yml --ask-become-pass --tags "deploy_back" ${ansible_use} \
		&& deactivate'

run-ansible-backup:
	@bash -c 'source ./venv/bin/activate && \
		ansible-playbook ./system_configuration_tools/provision-servers.yml --ask-become-pass --tags "backup" ${ansible_use} \
		&& deactivate'

run-ansible-preset_db:
	@bash -c 'source ./venv/bin/activate && \
		ansible-playbook ./system_configuration_tools/provision-servers.yml --ask-become-pass --tags "run_preset_db" ${ansible_use} \
		&& deactivate'

##### MAKEFILE COMMANDS #####

default:
	make setup-no-input
	make test

clean:
	rm -rf ./venv
	rm -rf ./src/vue/node_modules
	@if [ $(shell id "postgres" > /dev/null 2>&1; echo $$?) -eq 0 ]; then \
		make postgres-reset; \
	fi

##### DATABSE COMMANDS #####

postgres-reset:
	@sudo su -c "psql \
	-c \"DROP DATABASE IF EXISTS $(postgres_db)\" \
	-c \"DROP DATABASE IF EXISTS test_$(postgres_db)\" \
	-c \"DROP USER IF EXISTS $(postgres_dev_user)\" \
	" postgres

postgres-drop-development-db:
	@sudo su -c "psql -c \"DROP DATABASE IF EXISTS $(postgres_db)\"" postgres

postgres-init-development:
	@sudo su -c "psql \
	-c \"CREATE DATABASE $(postgres_db)\" \
	-c \"CREATE USER $(postgres_dev_user) WITH PASSWORD '$(postgres_dev_user_pass)'\" \
	-c \"ALTER ROLE $(postgres_dev_user) CREATEDB\" \
	-c \"ALTER ROLE $(postgres_dev_user) SET client_encoding TO 'utf8'\" \
	-c \"ALTER ROLE $(postgres_dev_user) SET default_transaction_isolation TO 'read committed'\" \
	-c \"ALTER ROLE $(postgres_dev_user) SET timezone TO 'CET'\" \
	-c \"GRANT ALL PRIVILEGES ON DATABASE $(postgres_db) TO $(postgres_dev_user)\" \
	-c \"alter role $(postgres_dev_user) superuser\" \
	" postgres

preset-db:
	@echo "This operation will wipe the $(postgres_db) database, press enter to continue (ctrl+c to cancel)"
	@read -r a
	make preset-db-no-input
preset-db-no-input:
	make postgres-reset
	make postgres-init-development
	make migrate-back
	bash -c 'source ./venv/bin/activate && cd ./src/django && python manage.py preset_db && deactivate'

migrate-back:
	bash -c "source ./venv/bin/activate && cd ./src/django && python manage.py makemigrations VLE && python manage.py migrate && deactivate"

migrate-merge:
	bash -c "source ./venv/bin/activate && cd ./src/django && python manage.py makemigrations --merge"

db-dump:
	@pg_dump --dbname=postgresql://$(postgres_dev_user):$(postgres_dev_user_pass)@127.0.0.1:5432/$(dbname) > db.dump
	@echo dump to file: db.dump success!

db-restore:
	@echo "This operation will wipe and then restore the $(postgres_db) database from db.dump, press enter to continue (ctrl+c to cancel)"
	@read -r a
	@sudo su -c "psql \
	-c \"DROP DATABASE IF EXISTS $(postgres_db)\" \
	-c \"DROP DATABASE IF EXISTS test_$(postgres_db)\" \
	-c \"CREATE DATABASE $(postgres_db)\" \
	" postgres
	@psql --dbname=postgresql://$(postgres_dev_user):$(postgres_dev_user_pass)@127.0.0.1:5432/$(dbname) < db.dump

##### MISC COMMANDS #####

superuser:
	bash -c 'source ./venv/bin/activate && python src/django/manage.py createsuperuser && deactivate'

update-dependencies:
	npm update --dev --prefix ./src/vue
	npm install --prefix ./src/vue

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

shell:
	bash -c 'source ./venv/bin/activate && cd ./src/django && python manage.py shell'

run-celery-worker-and-beat:
	bash -c 'sudo rabbitmqctl purge_queue celery && source ./venv/bin/activate && cd  ./src/django && celery -A VLE worker -l info -B'

encrypt_vault_var:
	bash -c 'source ./venv/bin/activate && ansible-vault encrypt_string "${inp}" --vault-password-file ./pass.txt'
