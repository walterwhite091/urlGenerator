start:
	python3 manage.py runserver
migrate:
	python3 manage.py makemigrations && python3 manage.py migrate
update:
	pip3 install -r requirements.txt