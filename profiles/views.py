from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from django.contrib.auth.models import User
from profiles.models import Profile, Professor, Student
from profiles.serializers import (
    ProfileSerializer,
    ProfessorSerializer,
    StudentSerializer,
)
import jwt
from monitoria.settings import SECRET_KEY
from django.test.client import Client
import ast
import json
from pdf_reader.LeitorPDF import getData


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
    except Profile.DoesNotExist:
        return Response(data={'error': "Erro terminal: Usuário sem perfil"},
                        status=HTTP_400_BAD_REQUEST)

    serializer = ProfileSerializer(profile)
    return Response(data=serializer.data, status=HTTP_200_OK)


@api_view(["POST"])
def set_profile(request):
    jwt_token = request.data.get('token')
    name = request.data.get('name')
    is_professor = request.data.get('is_professor')
    # Validação do token
    client = Client()
    response = client.post('/token_verify/', request.data)
    if response.status_code != HTTP_200_OK:
        return response
    # Decodificação do usuário
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=user_obj['user_id'])

    is_professor = ast.literal_eval(is_professor)

    # Obtendo profile
    if is_professor:
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile(user=user, is_professor=is_professor)
            profile.save()
            professor = Professor(profile=profile)
            professor.save()
        if name:
            profile.name = name
        profile.save()
        serializer = ProfileSerializer(profile)
    else:
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile(user=user, is_professor=is_professor)
            profile.save()
            student = Student(profile=profile)
            student.save()
        if name:
            profile.name = name
        profile.save()
        serializer = ProfileSerializer(profile)
    return Response(data=serializer.data, status=HTTP_200_OK)


@api_view(["POST"])
def registration(request):
    email = request.data.get('email')
    password = request.data.get('password')
    name = request.data.get('name')
    is_professor = request.data.get('is_professor')
    pdf_url = request.data.get('pdf_url')

    print('is_professor', is_professor)

    name = name if name is not None else ''
    email = email if email is not None else ''
    password = password if password is not None else ''
    is_professor = is_professor if is_professor is not None else False
    #pdf_url = pdf_url if pdf_url is not None else False

    print('is_professor', is_professor)

    user_data = {
        'email': email,
        'password1': password,
        'password2': password,
    }
    pdf_data = None
    if not is_professor and pdf_url!=None:
        # Necessario validar o pdf antes de prosseguir
        pdf_data = getData(pdf_url)
        try:
            if pdf_data['error']:
              return Response(data=pdf_data, status=HTTP_400_BAD_REQUEST)
        except:
            pass

    client = Client()
    response = client.post('/rest_registration/', user_data)
    if response.status_code != HTTP_201_CREATED:
        return response
        
    jwt_token = response.data['token']
    profile_data = {
        'token': jwt_token,
        'name': name,
        'is_professor': is_professor,
    }
    # Definir o perfil
    response = client.post('/set_profile/', profile_data)
    # Adicionar os dados do pdf ao perfil
    if not is_professor and pdf_data!=None:
        setStudentByData(pdf_data, jwt_token)
    
    return Response(data={'token': jwt_token,
                          'profile': response.data}, status=HTTP_201_CREATED)


@api_view(["POST"])
def get_professor(request):
    jwt_token = request.data.get('token')

    # Validação do token
    client = Client()
    response = client.post('/token_verify/', request.data)
    if response.status_code != HTTP_200_OK:
        return response
    # Decodificação do usuário
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=user_obj['user_id'])

    profile = Profile.objects.get(user=user)

    try:
        professor = Professor.objects.get(profile=profile)
    except Professor.DoesNotExist:
        return Response(data={'error': "Erro terminal: Este usuáro não possui perfil de professor"},
                        status=HTTP_400_BAD_REQUEST)

    serializer = ProfessorSerializer(professor)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(["POST"])
def professor_classes(request):
    jwt_token = request.data.get('token')
    str_classes = request.data.get('classes')
    classes = ast.literal_eval(str_classes)
    # Validação do token
    client = Client()
    response = client.post('/token_verify/', request.data)
    if response.status_code != HTTP_200_OK:
        return response
    # Decodificação do usuário
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=user_obj['user_id'])

    profile = Profile.objects.get(user=user)

    try:
        professor = Professor.objects.get(profile=profile)
    except Professor.DoesNotExist:
        return Response(data={'error': "Erro terminal: Este usuáro não possui perfil de professor"},
                        status=HTTP_400_BAD_REQUEST)

    professor.classes = classes
    professor.save()

    serializer = ProfessorSerializer(professor)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(["POST"])
def get_student(request):
    jwt_token = request.data.get('token')
    # Validação do token
    client = Client()
    response = client.post('/token_verify/', request.data)
    if response.status_code != HTTP_200_OK:
        return response
    # Decodificação do usuário
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=user_obj['user_id'])

    profile = Profile.objects.get(user=user)

    try:
        student = Student.objects.get(profile=profile)
    except Student.DoesNotExist:
        return Response(data={'error': "Erro terminal: Este usuáro não possui perfil de estudante"},
                        status=HTTP_400_BAD_REQUEST)

    serializer = StudentSerializer(student)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(["POST"])
def set_student(request):
    jwt_token = request.data.get('token')
    # Validação do token
    client = Client()
    response = client.post('/token_verify/', request.data)
    if response.status_code != HTTP_200_OK:
        return response
    # Decodificação do usuário
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=user_obj['user_id'])

    profile = Profile.objects.get(user=user)

    pdf_url = request.data.get('pdf_url')

    try:
        student = Student.objects.get(profile=profile)
    except Student.DoesNotExist:
        return Response(data={'error': "Erro terminal: Este usuáro não possui perfil de estudante"},
                        status=HTTP_400_BAD_REQUEST)

    student.pdf_url = pdf_url

    data = getData(pdf_url)
    try:
        if data['error'] != None:
            return Response(data=data, status=HTTP_400_BAD_REQUEST)
    except:
        pass

    student.matricula = data['matricula']
    student.ira = data['ira']
    student.academic_record = data['materias']
    
    student.save()

    serializer = StudentSerializer(student)
    return Response(serializer.data, status=HTTP_200_OK)

def setStudentByData(data, jwt_token):
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=user_obj['user_id'])

    profile = Profile.objects.get(user=user)

    try:
        student = Student.objects.get(profile=profile)
    except Student.DoesNotExist:
        return Response(data={'error': "Erro terminal: Erro durante a criação do estudante"},
                        status=HTTP_500_INTERNAL_SERVER_ERROR)

    student.matricula = data['matricula']
    student.ira = data['ira']
    student.academic_record = data['materias']

    student.save()

    return