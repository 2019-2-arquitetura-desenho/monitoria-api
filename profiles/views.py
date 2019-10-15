# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    # HTTP_403_FORBIDDEN,
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

unactive_profile = Response(data={'non_field_errors':'Perfil não existe'} ,status=HTTP_404_NOT_FOUND)

@api_view(["POST"])
def get_profile(request):
    jwt_token = request.data.get('token')

    # Validação do token
    client = Client()
    response = client.post('/token_verify/', request.data)
    if response.status_code != HTTP_200_OK:
        return response
    # Decodificação do usuário
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=user_obj['user_id'])

    try:
        profile = Profile.objects.get(user=user)
        if not profile.active:
            return unactive_profile
    except Profile.DoesNotExist:
        profile = Profile(user=user)
        profile.save()

    serializer = ProfileSerializer(profile)
    return Response(data=serializer.data, status=HTTP_200_OK)


@api_view(["POST"])
def set_profile(request):
    jwt_token = request.data.get('token')
    name = request.data.get('name')

    # Validação do token
    client = Client()
    response = client.post('/token_verify/', request.data)
    if response.status_code != HTTP_200_OK:
        return response
    # Decodificação do usuário
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=user_obj['user_id'])

    # Obtendo profile
    try:
        profile = Profile.objects.get(user=user)
        if not profile.active:
            return unactive_profile
    except Profile.DoesNotExist:
        profile = Profile(user=user)
        profile.save()
    if name:
        profile.name = name
    profile.save()
    serializer = ProfileSerializer(profile)
    return Response(data=serializer.data, status=HTTP_200_OK)

@api_view(["POST"])
def deactivate_profile(request):
    client = Client()
    jwt_token = request.data.get('token')

    # Validação do token
    response = client.post('/token_verify/', request.data)
    if response.status_code != HTTP_200_OK:
        return response
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=user_obj['user_id'])
    try:
        profile = Profile.objects.get(user=user)
        if not profile.active:
            return unactive_profile
    except Profile.DoesNotExist:
        profile = Profile(user=user)
        profile.save()
    profile.active = False
    profile.save()
    return Response(data={}, status=HTTP_200_OK)   

@api_view(["POST"])
def activate_profile(request):
    client = Client()
    jwt_token = request.data.get('token')

    # Validação do token
    response = client.post('/token_verify/', request.data)
    if response.status_code != HTTP_200_OK:
        return response
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=user_obj['user_id'])
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)
        profile.save()
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
