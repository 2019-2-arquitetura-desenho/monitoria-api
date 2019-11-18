#!/bin/sh
# entrypoint.sh

python3 /code/wait-for-postgres.py 
python3 manage.py makemigrations profiles
python3 manage.py makemigrations disciplines
python3 manage.py makemigrations 
python3 manage.py migrate
python3 manage.py migrate --run-syncdb
python3 manage.py runserver 0.0.0.0:8000
