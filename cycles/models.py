from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.



class Tripmodel(models.Model):
    id=models.IntegerField(primary_key=True,unique=True)
    customer_id=models.IntegerField()
    cycle_id=models.IntegerField()
    station_id=models.IntegerField()
    address=models.CharField(max_length=200)
    post_code=models.CharField(max_length=15)
    location_lat=models.FloatField()
    location_long=models.FloatField()

    class Meta:
        db_table='t_trips'

class Activetripmodel(models.Model):
    id=models.IntegerField(primary_key=True,unique=True)
    customer_id=models.IntegerField()
    cycle_id=models.IntegerField()
    station_id=models.IntegerField()
    address=models.CharField(max_length=200)
    post_code=models.CharField(max_length=15)
    location_lat=models.FloatField()
    location_long=models.FloatField()

    class Meta:
        db_table='t_active_trips'