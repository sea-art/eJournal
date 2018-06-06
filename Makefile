all: test

test: build
	echo "To be implemented: test..."

build: clean
	echo "To be implmented: build..."	

run-front: build
	python -mwebbrowser http://localhost:8080
	bash -c "source ./venv/bin/activate && npm run dev --prefix ./src/main/vue && deactivate"

run-back: build
	python -mwebbrowser http://localhost:8000
	bash -c "source ./venv/bin/activate && python3.6 ./src/main/django/manage.py runserver && deactivate"

clean:
		

cleansetup:
	rm -rf ./venv
	rm -rf ./src/main/vue/node_modules

setup: cleansetup
	#Install apt dependencies and ppa's.
	(sudo apt-cache show python3.6 | grep "Package: python3.6") || (sudo add-apt-repository ppa:deadsnakes/ppa -y; sudo apt update) || echo "0"
	sudo apt install npm nodejs git-flow python3.6 python3-pip python3.6-dev -y
	
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
	
	@echo "DONE!"
