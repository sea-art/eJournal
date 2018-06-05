all: test

test: build
	echo "To be implemented: test..."

build: clean
	echo "To be implmented: build..."	

run-front: build
	python -mwebbrowser http://localhost:8080
	npm run dev --prefix ./src/main/vue

run-back: build
	sudo service mysql start
	python -mwebbrowser http://localhost:8000
	pipenv run python3.6 ./src/main/django/manage.py runserver

clean:
	

setup:
	(sudo apt-cache show python3.6 | grep "Package: python3.6") || (sudo add-apt-repository ppa:deadsnakes/ppa -y; sudo apt update) || echo "0"
	sudo apt install npm nodejs python3.6 mysql-client mysql-server python3-pip python3.6-dev libmysqlclient-dev -y
	sudo service mysql start
	echo "CREATE DATABASE IF NOT EXISTS VLE;" | sudo mysql -uroot
	echo "DROP USER 'root'@'localhost';CREATE USER 'root'@'%' IDENTIFIED BY '';GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;FLUSH PRIVILEGES;"
	
	sudo pip3 install pipenv
	sudo pipenv sync
	
	npm cache clean -f
	npm config set strict-ssl false
	sudo npm install -g n
	npm config set strict-ssl true
	sudo n stable
	npm install --prefix ./src/main/vue vue-cli webpack
	npm install --prefix ./src/main/vue
	
	@echo "DONE!"
