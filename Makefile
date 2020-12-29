main: install
	sudo chmod 644 file_manager.service;
	sudo cp file_manager.service /etc/systemd/system/;
	sudo systemctl daemon-reload;
	sudo systemctl enable file_manager.service


install:
	sudo apt install python3-pip python3-dev curl;
	sudo pip3 install -r requirements.txt;
	python3 manage.py migrate;
	python3 manage.py collectstatic;


createsuperuser:
	python3 manage.py createsuperuser --username $(USERNAME) --noinput --email $(EMAIL)
	python3 manage.py drf_create_token $(USERNAME)
