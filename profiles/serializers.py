# from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    #pk = serializers.ReadOnlyField()
    #is_superuser = serializers.BooleanField()
    email = serializers.EmailField()


class ProfileSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()
    user = UserSerializer()
    name = serializers.CharField()
    

class StudentSerializer(serializers.Serializer):
    matricula = serializers.CharField()
    ira = serializers.FloatField()
    academic_record = serializers.ListField()

class ProfessorSerializer(serializers.Serializer):
    classes = serializers.ListField()
