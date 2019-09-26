from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from profiles.validators import validate_digit
from profiles.validators import validate_matlen

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    name = models.CharField(max_length=50)
    matricula = models.CharField(max_length=9, validators=[validate_digit, validate_matlen])
    ira = models.FloatField()

