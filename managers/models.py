from django.db import models

# Create your models here.

from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django import forms

# Create your models here.

class Managermodel(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    hashed_password=models.CharField(max_length=200)
    phone=models.CharField(max_length=50)
    session_id=models.IntegerField(null=True)

    class Meta:
        db_table='t_managers'
    
class Managessionmodel(models.Model):
    id=models.AutoField(primary_key=True)
    manager_id=models.IntegerField()
    access_token=models.CharField(max_length=200)

    class Meta:
        db_table='t_manager_sessions'