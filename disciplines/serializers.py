from rest_framework import serializers

class ClassSerializer(serializers.Serializer):
    pass

class DisciplineSerializer(serializers.Serializer):
    cod = serializers.IntegerField()
    name = serializers.CharField()
    credts = serializers.IntegerField()
    classes =  serializers.ListField()

