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
from profiles.models import Professor, Student, Profile

def get_user(jwt_token):
    if not jwt_token:
        return Response(data={'token': "Esse campo é obrigarório"},
                        status=HTTP_400_BAD_REQUEST), None
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

def get_profile(jwt_token):
    response, user = get_user(jwt_token)
    if response.status_code!=HTTP_200_OK:
        return response, None
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return Response(data={'error': "Erro terminal: Falha ao localizar perfil"},
                        status=HTTP_400_BAD_REQUEST), None
    if profile.is_professor:
        try:
            professor = Professor.objects.get(profile=profile)
            return Response(status=HTTP_200_OK), professor 
        except Professor.DoesNotExist:
            return Response(data={'error': "Erro terminal: Falha ao localizar estudante"},
                                status=HTTP_400_BAD_REQUEST), None
    else:
        try:
            student = Student.objects.get(profile=profile)
            return Response(status=HTTP_200_OK), student 
        except Student.DoesNotExist:
            return Response(data={'error': "Erro terminal: Falha ao localizar estudante"},
                                status=HTTP_400_BAD_REQUEST), None