all: test

test: build
	pep8 ./src/main/django --max-line-length=120
	pep8 ./src/test/django --max-line-length=120
	bash -c "source ./venv/bin/activate && ./src/main/django/manage.py test ./src/test/django && deactivate"
	npm run lint --prefix ./src/main/vue
	npm run test --prefix ./src/main/vue
	npm run unit --prefix ./src/main/vue

build: clean
	echo "To be implmented: build..."	

run-front: build
	python -mwebbrowser http://localhost:8080
	bash -c "source ./venv/bin/activate && npm run dev --prefix ./src/main/vue && deactivate"

run-back: build
	sudo service mysql start
	python -mwebbrowser http://localhost:8000
	bash -c "source ./venv/bin/activate && python3.6 ./src/main/django/manage.py runserver && deactivate"

clean:
		

cleansetup:
	rm -rf ./venv
	rm -rf ./src/main/vue/node_modules

setup: cleansetup
	#Install apt dependencies and ppa's.
	(sudo apt-cache show python3.6 | grep "Package: python3.6") || (sudo add-apt-repository ppa:deadsnakes/ppa -y; sudo apt update) || echo "0"
	sudo apt install npm nodejs git-flow python3.6 mysql-client mysql-server python3-pip python3.6-dev libmysqlclient-dev -y
	
	#Install dependencies for python (django, etc).
	sudo pip3 install virtualenv
	virtualenv -p python3.6 venv
	bash -c 'source ./venv/bin/activate && pip install -r requirements.txt && deactivate'
	
	#Update n & install nodejs dependencies.
	npm cache clean -f
	npm config set strict-ssl false
	sudo npm install -g n
	npm config set strict-ssl true
	sudo n stable
	npm install --prefix ./src/main/vue vue-cli webpack
	npm install --prefix ./src/main/vue
		
	sudo service mysql start
	(echo "CREATE DATABASE IF NOT EXISTS VLE;" | sudo mysql -uroot) || (echo "CREATE DATABASE IF NOT EXISTS VLE;" | sudo mysql -uroot -p)

	@echo "DONE!"

fixsql:
	#Try to fix SQL by forcing privileges
	sudo service mysql start
	(echo "DROP USER 'root'@'localhost';CREATE USER 'root'@'%' IDENTIFIED BY '';GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;FLUSH PRIVILEGES;" | sudo mysql -uroot) || (echo "DROP USER 'root'@'localhost';CREATE USER 'root'@'%' IDENTIFIED BY '';GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;FLUSH PRIVILEGES;" | sudo mysql -uroot -p) || (python -mwebbrowser https://bit.ly/2xNbNMc)
