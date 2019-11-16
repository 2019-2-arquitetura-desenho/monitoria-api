#!/bin/sh
# entrypoint.sh

python3 /code/wait-for-postgres.py 
python3 manage.py runserver 0.0.0.0:8000