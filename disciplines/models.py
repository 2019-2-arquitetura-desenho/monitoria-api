from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import timedelta
from django.utils import timezone
from profiles.models import Student

class Discipline(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250, default='')

class Period(models.Model):
    id = models.AutoField(primary_key=True)
    initial_time = models.DateField(default=timezone.now().date())
    end_time = models.DateField(default=timezone.now().date()+timedelta(days=30))   

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, default='')
    shift = models.CharField(max_length=40, default='')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    professors = ArrayField(models.CharField(max_length=250), default=list)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, null=True)

class ClassRegister(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    points = models.FloatField(default=0.0)
    discipline_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    indication = models.FloatField(null=True, blank=True)
    priority = models.IntegerField(default=1)