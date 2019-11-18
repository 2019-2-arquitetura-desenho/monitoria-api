# #!/bin/sh
# # entrypoint.sh

# # python /code/wait-for-postgres.py 
# python manage.py makemigrations
# python manage.py migrate
# python manage.py migrate --run-syncdb
# python manage.py runserver