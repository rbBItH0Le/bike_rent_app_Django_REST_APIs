from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.postgres.fields import ArrayField
# Create your models here.



class Cyclemodel(models.Model):
    cycle_id=models.AutoField(primary_key=True)
    station_id=models.IntegerField()
    category=models.CharField(max_length=15)
    is_charging=models.CharField(max_length=10,null=True)
    battery_percentage=models.CharField(max_length=10,null=True)
    model_number=models.CharField(max_length=15,null=True)
    status_id=models.IntegerField(null=True)
        
    class Meta:
        db_table='t_cycles'

class Tripmodel(models.Model):
    rip_id=models.AutoField(primary_key=True,unique=True)
    customer_id=models.IntegerField()
    cycle_id=models.IntegerField()
    model_number=models.CharField(max_length=15,null=True)
    station_id=models.IntegerField()
    address=models.CharField(max_length=200)
    post_code=models.CharField(max_length=15)
    location_lat=models.FloatField()
    location_long=models.FloatField()
    started_at=models.BigIntegerField(null=True)
    ended_at=models.BigIntegerField(null=True)
    charge=models.IntegerField(null=True)

    class Meta:
        db_table='t_trips'

class Activetripmodel(models.Model):
    active_trip_id=models.AutoField(primary_key=True,unique=True)
    customer_id=models.IntegerField()
    cycle_id=models.IntegerField()
    model_number=models.CharField(max_length=15,null=True)
    station_id=models.IntegerField()
    address=models.CharField(max_length=200)
    post_code=models.CharField(max_length=15)
    location_lat=models.FloatField()
    location_long=models.FloatField()
    started_at=models.BigIntegerField(null=True)
    ended_at=models.BigIntegerField(null=True)

    class Meta:
        db_table='t_active_trips'
