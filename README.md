# Monitoria-API

Repositório destinado a API da aplicação "A Monitoria".

## Execução

Inicializar Aplicação:

    make server

Para inicializar o bash do container, após subir o container:

    make bash

## Configurações de Ambiente

Para utilizar a API, crie um arquivo .env na raiz do projeto, e dentro:

    DOMAIN=localhost:8000
    PASSWORD_EMAIL=NeedToBeSetInEnvFile
    SECRET_KEY=o^gxy879i$y^k+r1lo%*!0(-^er)jnos9qtg$zm%qs&de03n&!
    HEROKU_URL=http://amonitoria-offers.herokuapp.com