main: install
	sudo cp file_manager.service /etc/systemd/system/;
	sudo systemctl start file_manager;
	sudo systemctl enable file_manager

install:
	sudo apt install python3-pip python3-dev curl;
	pip3 install -r requirements.txt;
	python3 manage.py migrate
