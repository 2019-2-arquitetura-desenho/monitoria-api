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
def create_profile(request):
    jwt_token = request.data.get('token')
    matricula = request.data.get('matricula')
    name = request.data.get('name')
    ira = request.data.get('ira')
    if not name or not matricula or not ira or not jwt_token:
            return Response(data={'erro':'Um ou mais campos vazios'}, status=HTTP_404_NOT_FOUND)    
    client = Client()
    response = client.post('/token_verify/', request.data)
    if response.status_code<200 or response.status_code>=300:
        return Response(data={'error': 'Token invalido'} ,status=HTTP_403_FORBIDDEN)
    
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=user_obj['user_id'])
    try:
        student = Student.objects.get(user=user)
        print(student.matricula)
        return Response(data={'error':'Já existe perfil para esse usuário'}, status=HTTP_404_NOT_FOUND)
    except Student.DoesNotExist:
        try:
            validate_ira(ira)
        except:
            return Response(data={'error':'Valor inválido para o ira'}, status=HTTP_404_NOT_FOUND)
        try:
            validate_mat(matricula)
        except:
            return Response(data={'error':'Valor inválido para a matrícula'}, status=HTTP_404_NOT_FOUND)
        student = Student(user=user, name=name, matricula=matricula, ira=ira)
        student.save()
    serializer = StudentSerializer(student)

    return Response(data=serializer.data, status=HTTP_200_OK)

@api_view(["POST"])
def set_profile(request):
    jwt_token = request.data.get('token')
    matricula = request.data.get('matricula')
    name = request.data.get('name')
    ira = request.data.get('ira')
    client = Client()
    response = client.post('/token_verify/', request.data)
    if response.status_code<200 or response.status_code>=300:
        return Response(data={'error': 'Token invalido'} ,status=HTTP_403_FORBIDDEN)
    
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=user_obj['user_id'])
    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        return Response(data={'error':'Não existe perfil para esse usuário'}, status=HTTP_404_NOT_FOUND)
    if ira:
        try:
            validate_ira(ira)
            student.ira=ira
        except:
            return Response(data={'error':'Valor inválido para o ira'}, status=HTTP_404_NOT_FOUND)
    if matricula:
        try:
            validate_mat(matricula)
            student.matricula=matricula
        except:
            return Response(data={'error':'Valor inválido para a matrícula'}, status=HTTP_404_NOT_FOUND)
    if name:
        student.name = name
    student.save()
    serializer = StudentSerializer(student)
    return Response(data=serializer.data, status=HTTP_200_OK)
        
   
        
    

    