from rest_framework import serializers
from disciplines.models import Class
from disciplines.models import Discipline

class DisciplineSerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.IntegerField()

class ClassSerializer(serializers.Serializer):
    name = serializers.CharField()
    shift = serializers.CharField()
    discipline = DisciplineSerializer()


# class ClassSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Class
#         fields = ['name', 'shift', 'discipline']
