from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)
from django.contrib.auth.models import User
import jwt
import requests
from rest_framework_jwt.views import verify_jwt_token
from django.test.client import Client

@api_view(["POST"])
def set_profile(request):
    jwt_token = request.data.get('token')
    print(jwt_token)
    c = Client()
    response = c.post('/login/', {'token': jwt_token})
    if response.status_code>=200 and response.status_code<300:
        return Response(data={'alo': 'ok'},status=HTTP_200_OK)
    else:
        return Response(data={'alo': 'deu ruim'},status=HTTP_200_OK)