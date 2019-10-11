from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)
from django.contrib.auth.models import User
from profiles.serializers import UserSerializer
from profiles.models import Student
from profiles.serializers import StudentSerializer
import jwt
import requests
from monitoria.settings import SECRET_KEY
from rest_framework_jwt.views import verify_jwt_token
from django.test.client import Client
from profiles.validators import validate_ira
from profiles.validators import validate_mat

@api_view(["POST"])
def get_profile(request):
    jwt_token = request.data.get('token')

    #Validação do token
    client = Client()
    response = client.post('/token_verify/', request.data)
    if response.status_code!=HTTP_200_OK:
        return response
    # Decodificação do usuário
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=user_obj['user_id'])

    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        student = Student(user=user)
        student.save()

    serializer = StudentSerializer(student)
    return Response(data=serializer.data, status=HTTP_200_OK)

@api_view(["POST"])
def set_profile(request):
    jwt_token = request.data.get('token')
    matricula = request.data.get('matricula')
    name = request.data.get('name')
    ira = request.data.get('ira')

    #Validação do token
    client = Client()
    response = client.post('/token_verify/', request.data)
    if response.status_code!=HTTP_200_OK:
        return response
    # Decodificação do usuário
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=user_obj['user_id'])

    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        student = Student(user=user)
        student.save()

    if ira:
        try:
            validate_ira(ira)
            student.ira=ira
        except ValidationError:
            return Response(data={'error':'Valor inválido para o ira'}, status=HTTP_400_BAD_REQUEST)

    if matricula:
        try:
            validate_mat(matricula)
            student.matricula=matricula
        except ValidationError:
            return Response(data={'error':'Valor inválido para a matrícula'}, status=HTTP_400_BAD_REQUEST)

    if name:
        student.name = name
    student.save()
    serializer = StudentSerializer(student)
    return Response(data=serializer.data, status=HTTP_200_OK)

@api_view(["POST"])
def registration(request):
    email = request.data.get('email')
    password = request.data.get('password')
    name = request.data.get('name')
    user_data = {
        'email': email,
        'password1':password,
        'password2':password,
    }
    client = Client()
    response = client.post('/rest_registration/', user_data)
    if response.status_code!=HTTP_201_CREATED:
        return response
    jwt_token = response.data['token']
    print(jwt_token)
    profile_data = {
        'token':jwt_token,
        'name':name    
    }
    response = client.post('/set_profile/', profile_data)
    return response
    

        
   
        
    

    