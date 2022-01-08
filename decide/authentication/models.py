from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Persona(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    sexo = models.CharField(max_length=30, blank=False)
    ip = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    edad = models.PositiveSmallIntegerField()
