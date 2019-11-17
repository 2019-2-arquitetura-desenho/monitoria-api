from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from django.contrib.auth.models import User
import jwt
from monitoria.settings import SECRET_KEY
from django.test.client import Client
import ast
import json


def get_user(jwt_token):
    client = Client()
    response = client.post('/token_verify/', {'token':jwt_token})
    if response.status_code != HTTP_200_OK:
        return response, None
    # Decodificação do usuário
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    try:
        user = User.objects.get(pk=user_obj['user_id'])
        return Response(status=HTTP_200_OK), user
    except User.DoesNotExist:
        return Response(data={'error': "Usuário nao cadastrado"},
                        status=HTTP_400_BAD_REQUEST), None
    