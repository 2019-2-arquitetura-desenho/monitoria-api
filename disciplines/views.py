from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from disciplines.models import Class, Discipline
from disciplines.serializers import ClassSerializer, DisciplineSerializer
from rest_framework import viewsets

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
# Create your views here.
