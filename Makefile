all: test

test: build
	echo "To be implemented: test..."

build: clean
	echo "To be implmented: build..."	

run-front: build
	npm run dev --prefix ./src/main/vue

run-back: build
	sudo service mysql start
	pipenv run python ./src/main/django/manage.py runserver

clean:
	echo "To be implemented: clean..."

setup:
	sudo apt install npm python3 mysql-client mysql-server python3-pip python3-dev libmysqlclient-dev -y
	pip3 install pipenv
	pipenv sync
	sudo npm cache clean -f
	sudo npm install -g n
	sudo n stable
	sudo npm install -g vue-cli	
	npm install --prefix ./src/main/vue
