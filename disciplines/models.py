from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import timedelta
from django.utils import timezone
from profiles.models import Student

class Discipline(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250, default='')

class Period(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    initial_time = models.DateField(default=timezone.now().date())
    end_time = models.DateField(default=timezone.now().date()+timedelta(days=30))

class Meeting(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    day = models.CharField(max_length=250)
    init_hour = models.CharField(max_length=250)
    final_hour = models.CharField(max_length=250)
    room = models.CharField(max_length=250)

class Class(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=250, default='')
    vacancies = models.IntegerField(default=0)
    shift = models.CharField(max_length=40, default='')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    professors = ArrayField(models.CharField(max_length=250), default=list)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, null=True)
    meetings = models.ManyToManyField(Meeting)

class ClassRegister(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    points = models.FloatField(default=0.0)
    discipline_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    indication = models.FloatField(null=True, blank=True)
    priority = models.IntegerField(default=1)
    status = models.CharField(max_length=50, default='Indefinido')

