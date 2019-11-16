from rest_framework import serializers

class DisciplineSerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.IntegerField()

class PeriodSerializer(serializers.Serializer):
    initial_time = serializers.DateField()
    end_time = serializers.DateField()

class ClassSerializer(serializers.Serializer):
    name = serializers.CharField()
    shift = serializers.CharField()
    discipline = DisciplineSerializer()
    professors = serializers.ListField()
    period = PeriodSerializer()