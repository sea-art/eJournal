all: test

test: build
	echo "To be implemented: test..."

build: clean
	echo "To be implmented: build..."	

run-front: build
	npm run dev --prefix ./src/main/vue

run-back: build
	sudo service mysql start
	pipenv run python3.6 ./src/main/django/manage.py runserver

clean:
	

setup:
	(sudo apt-cache show python3.6 | grep "Package: python3.6") || (sudo add-apt-repository ppa:deadsnakes/ppa -y; sudo apt update) || 0
	sudo apt install npm nodejs python3.6 mysql-client mysql-server python3-pip python3.6-dev libmysqlclient-dev -y
	
	sudo pip3 install pipenv
	sudo pipenv sync
	
	npm cache clean -f
	npm config set strict-ssl false
	#sudo npm install -g npm
	sudo npm install -g n
	npm config set strict-ssl true
	sudo n stable
	npm install --prefix ./src/main/vue vue-cli webpack
	npm install --prefix ./src/main/vue
	echo "CREATE DATABASE IF NOT EXISTS VLE;" | mysql -uroot
	@echo "DONE!"
