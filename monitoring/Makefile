setup:
	@echo "This operation will clean old files, press enter to continue (ctrl+c to cancel)"
	@read -r a
	@make clean
	make setup-venv requirements_file=local.txt

setup-venv:
	sudo pip3 install virtualenv
	virtualenv -p python3 venv
	bash -c '\
		source ./venv/bin/activate && \
		pip install -r requirements/$(requirements_file) && \
		deactivate'

clean:
	rm -rf ./venv

provision-monitoring:
	@source venv/bin/activate && ansible-playbook ansible/provision-monitoring.yml && deactivate
