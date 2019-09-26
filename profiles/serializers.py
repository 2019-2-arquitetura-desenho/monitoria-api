from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    email = serializers.EmailField()

class StudentSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    user = UserSerializer()
    name = serializers.CharField()
    matricula = serializers.CharField()
    ira = serializers.FloatField()