from django.db import models
from django.contrib.auth.models import User
# from profiles.validators import validate_mat


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    name = models.CharField(max_length=50, default='')
    matricula = models.CharField(max_length=9, blank=True, null=True)
    ira = models.FloatField(blank=True, null=True)
