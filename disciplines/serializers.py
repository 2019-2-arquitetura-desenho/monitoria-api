from rest_framework import serializers
from profiles.serializers import StudentShortSerializer

class DisciplineSerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.IntegerField()

class PeriodSerializer(serializers.Serializer):
    initial_time = serializers.DateField()
    end_time = serializers.DateField()

class MeetingSerializer(serializers.Serializer):
    day = serializers.CharField()
    init_hour = serializers.CharField()
    final_hour = serializers.CharField()
    room = serializers.CharField()

class ClassSerializer(serializers.Serializer):
    name = serializers.CharField()
    shift = serializers.CharField()
    discipline = DisciplineSerializer()
    professors = serializers.ListField()
    #period = PeriodSerializer()
    meetings = MeetingSerializer(many=True)

class ClassShortSerializer(serializers.Serializer):
    name = serializers.CharField()
    discipline = DisciplineSerializer()

class ClassRegisterSerializer(serializers.Serializer):
    student = StudentShortSerializer()
    points = serializers.FloatField()
    discipline_class = ClassShortSerializer()
    indication = serializers.FloatField()
    priority = serializers.IntegerField()
