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
    # try:
    response = urllib.request.urlopen(HEROKU_URL+'/discipline/?format=json')
    data = json.loads(response.read())
    # except:
    #     return Response(data={'error': "Erro terminal: Erro durante a comunicação com o Crawler"},
    #                     status=HTTP_400_BAD_REQUEST)

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
