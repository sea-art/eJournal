
superuser:
	bash -c 'source ./venv/bin/activate && python3.6 src/django/manage.py createsuperuser && deactivate'

test-back:
	pep8 ./src/django --max-line-length=120 --exclude='./src/django/VLE/migrations','./src/django/VLE/settings*'
	make test-flake
	bash -c "source ./venv/bin/activate && cd ./src/django/ && python3.6 manage.py test && deactivate"

test-front:
	npm run lint --prefix ./src/vue
	npm run test --prefix ./src/vue

test-flake:
	bash -c 'source ./venv/bin/activate && flake8 --max-line-length=120 src/django --exclude="src/django/VLE/migrations/*","src/django/VLE/settings/*","src/django/VLE/settings.py" && deactivate'

test: test-back test-front

fill-db: migrate-back
	bash -c 'source ./venv/bin/activate && cd ./src/django && echo "delete from sqlite_sequence where name like \"VLE_%\";" | sqlite3 VLE.db && python3.6 manage.py flush --no-input && python3.6 manage.py preset_db && deactivate'

demo-db: migrate-back
	bash -c 'source ./venv/bin/activate && cd ./src/django && echo "delete from sqlite_sequence where name like \"VLE_%\";" | sqlite3 VLE.db && python3.6 manage.py flush --no-input && python3.6 manage.py demo_db && deactivate'

random-db: fill-db
	bash -c 'source ./venv/bin/activate && cd ./src/django && python3.6 manage.py random_db && deactivate'

show-db:
	bash -c 'source ./venv/bin/activate && cd ./src/django && python3.6 manage.py show_db && deactivate'

migrate-back:
	bash -c "source ./venv/bin/activate && cd ./src/django && (rm VLE.db || echo "0") && python3.6 manage.py makemigrations VLE && python3.6 manage.py migrate && deactivate"

run-front:
	python -mwebbrowser http://localhost:8080
	bash -c "source ./venv/bin/activate && npm run dev --prefix ./src/vue && deactivate"

run-back:
	bash -c "source ./venv/bin/activate && python3.6 ./src/django/manage.py runserver && deactivate"

clean:
	rm -rf ./venv
	rm -rf ./src/vue/node_modules
	rm -rf ./src/django/VLE/migrations
	rm -rf ./src/django/VLE.db

fixnpm:
	npm cache clean -f
	npm config set strict-ssl false
	sudo npm install -g n
	npm config set strict-ssl true
	sudo n stable

setup:
	#Install apt dependencies and ppa's.
	(sudo apt-cache show python3.6 | grep "Package: python3.6") || (sudo add-apt-repository ppa:deadsnakes/ppa -y; sudo apt update) || echo "0"
	sudo apt install npm nodejs git-flow python3.6 python3-pip pep8 sqlite3 -y

	make clean

	#Install dependencies for python (django, etc).
	sudo pip3 install virtualenv
	virtualenv -p python3.6 venv
	bash -c 'source ./venv/bin/activate && pip install git+https://github.com/joestump/python-oauth2.git && pip install -r requirements.txt && deactivate'

	#Update n & install nodejs dependencies.
	npm install --prefix ./src/vue

	#Initialize the database
	make fill-db

	@echo "DONE!"


deploy:
	chmod +x deploy.sh
	sudo ./deploy.sh

deploy-fresh:
	chmod +x deploy.sh
	sudo ./deploy.sh fresh
