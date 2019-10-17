# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    # HTTP_400_BAD_REQUEST,
)
from django.contrib.auth.models import User
# from profiles.serializers import UserSerializer
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
import jwt
# import requests
from monitoria.settings import SECRET_KEY
# from rest_framework_jwt.views import verify_jwt_token
from django.test.client import Client
# from profiles.validators import validate_ira
# from profiles.validators import validate_mat
# from django.core.exceptions import ValidationError

UNACTIVE_PROFILE = Response(data={'non_field_errors':['Perfil não existe']} ,status=HTTP_404_NOT_FOUND)
UNACTIVE_USER = Response(data={'non_field_errors':['Usuário não existe']} ,status=HTTP_404_NOT_FOUND)

# Valida o token e retorna profile associado caso tenha sucesso
# Caso contrário retorna False e o response de erro
def valide_token(jwt_token):
    client = Client()
    response = client.post('/token_verify/', {'token':jwt_token})
    if response.status_code == HTTP_200_OK:
        user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        try:
            user = User.objects.get(pk=user_obj['user_id'])
        except User.DoesNotExist:
            return False, UNACTIVE_USER
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile(user=user)
        profile.save()
        return True, profile
    return False, response


@api_view(["POST"])
def get_profile(request):
    jwt_token = request.data.get('token')
    # Validação do token
    status, response = valide_token(jwt_token)
    
    if status==False:
        return response
    profile = response
    if not profile.active:
        return UNACTIVE_PROFILE
    serializer = ProfileSerializer(profile)
    return Response(data=serializer.data, status=HTTP_200_OK)


@api_view(["POST"])
def set_profile(request):
    jwt_token = request.data.get('token')
    name = request.data.get('name')

    # Validação do token
    status, response = valide_token(jwt_token)
    if status==False:
        return response
    profile = response

    if not profile.active:
        return UNACTIVE_PROFILE

    if name:
        profile.name = name
    profile.save()
    serializer = ProfileSerializer(profile)
    return Response(data=serializer.data, status=HTTP_200_OK)

@api_view(["POST"])
def deactivate_profile(request):
    jwt_token = request.data.get('token')

    # Validação do token
    status, response = valide_token(jwt_token)
    if status==False:
        return response
    profile = response

    profile.active = False
    profile.save()
    return Response(data={}, status=HTTP_200_OK)   

@api_view(["POST"])
def activate_profile(request):
    jwt_token = request.data.get('token')

    # Validação do token
    status, response = valide_token(jwt_token)
    if status==False:
        return response
    profile = response

    profile.active = True
    profile.save()
    return Response(data={}, status=HTTP_200_OK)   

@api_view(["POST"])
def registration(request):
    email = request.data.get('email')
    password = request.data.get('password')
    name = request.data.get('name')
    name = name if name is not None else ''
    email = email if email is not None else ''
    password = password if password is not None else ''
    user_data = {
        'email': email,
        'password1': password,
        'password2': password,
    }
    client = Client()
    response = client.post('/rest_registration/', user_data)
    if response.status_code != HTTP_201_CREATED:
        return response
    jwt_token = response.data['token']
    profile_data = {
        'token': jwt_token,
        'name': name
    }
    response = client.post('/set_profile/', profile_data)
    return Response(data={'token': jwt_token,
                    'profile': response.data}, status=HTTP_201_CREATED)
