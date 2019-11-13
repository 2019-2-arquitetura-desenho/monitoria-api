from rest_framework import serializers
from disciplines.models import Class
from disciplines.models import Discipline

class ClassSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Class
        fields = ['name', 'room', 'schedule', 'shift', 'professors']

class DisciplineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Discipline
        fields = ['name', 'cod', 'credts', 'classes']
