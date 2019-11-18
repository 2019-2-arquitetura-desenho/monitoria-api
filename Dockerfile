FROM python:3-alpine3.10
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev 
RUN pip3 install --upgrade pip
RUN pip3 install psycopg2
RUN apk add build-base
RUN apk add poppler-dev
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code
RUN pip3 install -r requirements.txt
ADD . /code
ENV PYTHONPATH "."
CMD gunicorn monitoria.wsgi:application --bind 0.0.0.0:$PORT
# ENTRYPOINT [ "/bin/sh", "entrypoint.sh" ]