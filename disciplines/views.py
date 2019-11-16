from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from disciplines.models import Class, Discipline, Period
from disciplines.serializers import ClassSerializer, DisciplineSerializer, PeriodSerializer
from rest_framework import viewsets
from django.utils import timezone
from monitoria.settings import SECRET_KEY, HEROKU_URL
import urllib
import json
import jwt
from django.test.client import Client
from profiles.models import Student, Profile, Professor, User

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer

@api_view(["POST"])
def get_discipline(request):
    pass

@api_view(["POST"])
def add_professor(request):
    pass

@api_view(["POST"])
def get_professor(request):
    pass

@api_view(["POST"])
def remove_professor(request):
    pass

@api_view(["POST"])
def create_period(request):
    initial_time = request.data.get('initial_time')
    end_time = request.data.get('end_time')

    # Colocar as disciplinas neste periodo
    try:
        response = urllib.request.urlopen(HEROKU_URL+'/discipline/?format=json')
        data = json.loads(response.read())
    except:
        return Response(data={'error': "Erro terminal: Erro durante a comunicação com o Crawler"},
                        status=HTTP_400_BAD_REQUEST)

    period = Period()
    if initial_time:
        period.initial_time=initial_time
    if end_time:
        period.end_time=end_time

    period.save()

    for discipline in data:
        temp_discipline = Discipline()
        temp_discipline.name = discipline['name']
        temp_discipline.code = discipline['code']
        temp_discipline.save()
        for each in discipline['discipline_class']:
            temp_class = Class()
            temp_class.name = each['name']
            temp_class.vacancies = each['vacancies']
            temp_class.shift = each['shift']
            temp_class.professors = []
            for professor in each['teachers']:
                temp_class.professors.append(professor['name'])

            temp_class.discipline = temp_discipline
            temp_class.period = period
            temp_class.save()

    serializer = PeriodSerializer(period)
    return Response(data=serializer.data, status=HTTP_200_OK)

@api_view(["POST"])
def register_discipline(request):
    jwt_token = request.data.get('token')
    discipline_code = request.data.get('discipline_code')
    class_name = request.data.get('class_name')
    # Validação do token
    client = Client()
    response = client.post('/token_verify/', request.data)
    if response.status_code != HTTP_200_OK:
        return response
    # Decodificação do usuário
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    
    try:
        user = User.objects.get(pk=user_obj['user_id'])
        profile = Profile.objects.get(user=user)
        student = Student.objects.get(profile=profile)
    except (Student.DoesNotExist, Profile.DoesNotExist, User.DoesNotExist):
        return Response(data={'error': "Erro terminal: Falha ao localizar perfil"},
                        status=HTTP_400_BAD_REQUEST)

    try:
        discipline = Discipline.objects.get(code=discipline_code)
    except:
        return Response(data={'error': "Erro terminal: Falha ao localizar disciplina"},
                        status=HTTP_400_BAD_REQUEST)

    try:
        temp_class = Class.objects.filter(discipline=discipline).get(name=class_name)
    except:
        return Response(data={'error': "Erro terminal: Falha ao localizar turmas"},
                        status=HTTP_400_BAD_REQUEST)

    for each in temp_class.ranking:
        if each[1]==student.matricula:
            return Response(data={'error': "Estudante ja esta cadastrado na turma"},
                        status=HTTP_400_BAD_REQUEST)

    for each in student.academic_record:
        if each[0]==str(discipline.code):
            # COMO EU CALCULO ISSO
            values = {
                "SS": 5,
                "MS": 4,
                "MM": 3,
            }
            value = (values[each[1]]*0.6) + (student.ira*0.4)
            value = str(value)
            temp_class.ranking.append([value, student.matricula])
            temp_class.save()
            serializer = ClassSerializer(temp_class)
            return Response(data=serializer.data, status=HTTP_200_OK)

    return Response(data={'error': "Erro terminal: Estudante nao realizou esta disciplina"},
                        status=HTTP_400_BAD_REQUEST)

    