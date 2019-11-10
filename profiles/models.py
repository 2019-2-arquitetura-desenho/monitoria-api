from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
# from profiles.validators import validate_mat

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    name = models.CharField(max_length=50, default='')
    is_professor = models.BooleanField(default=False)

class Student(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True,)
    matricula = models.CharField(max_length=9, blank=True, null=True)
    ira = models.FloatField(blank=True, null=True)
    academic_record = ArrayField(ArrayField(models.CharField(max_length=10), size=2), default=list)
    
class Professor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True,)
    classes = ArrayField(ArrayField(models.CharField(max_length=10), size=2), default=list)
    