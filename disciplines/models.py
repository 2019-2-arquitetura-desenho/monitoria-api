from django.db import models
from django.contrib.postgres.fields import ArrayField

class Class(models.Model):
    name = models.CharField(max_length=50, default='')
    room = models.CharField(max_length=50, default='')
    schedule = ArrayField(models.CharField(max_length=30))
    shift = models.CharField(max_length=50, default='')
    professors = ArrayField(models.IntegerField())

class Discipline(models.Model):
    cod = models.IntegerField(default=0)
    name = models.CharField(max_length=50, default='')
    credts = models.IntegerField(default=0)
    classes =  ArrayField(models.IntegerField())

# Create your models here.
