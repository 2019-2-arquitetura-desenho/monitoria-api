from django.db import models
from django.contrib.auth.models import User
from profiles.validators import validate_mat

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    name = models.CharField(max_length=50)
    matricula = models.CharField(max_length=9, validators=[ validate_mat ])
    ira = models.FloatField()

