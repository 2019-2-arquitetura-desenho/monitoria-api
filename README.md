# monitoria-api
Repositório destinado a API da aplicação "A Monitoria".

## Execução

Inicializar serviço do docker:

    make start-docker

Caso não dê certo, use:

    make start-docker2

Inicializar Aplicação:

    make server

Para inicializar o bash do container, após subir o container:

    make bash

Para rodar as migrations:

    make bash
    python3 manage.py makemigrations
    python3 manage.py migrate