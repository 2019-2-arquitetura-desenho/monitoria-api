from django.db import models
from django.contrib.postgres.fields import ArrayField

class Discipline(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, default='')

    
class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='')
    shift = models.CharField(max_length=40, default='')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)

# Create your models here.
