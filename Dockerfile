FROM python:3-alpine3.10
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR /code
ADD . /code