from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.



class Operatormodel(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    hashed_password=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    session_id=models.IntegerField(null=True)

    class Meta:
        db_table='t_operators'

class Operatsessionmodel(models.Model):
        id=models.AutoField(primary_key=True)
        operator_id=models.IntegerField()
        access_token=models.CharField(max_length=200)

        class Meta:
            db_table='t_operator_sessions'


class Stationmodel(models.Model):
        station_id=models.AutoField(primary_key=True)
        capacity=models.IntegerField()
        availability=models.IntegerField()
        address=models.CharField(max_length=200)
        post_code=models.CharField(max_length=10)
        location_lat=models.FloatField()
        location_long=models.FloatField()
        serialised_plan=models.CharField(max_length=300)

        class Meta:
            db_table='t_stations'


class Errormodel(models.Model):
        error_code=models.IntegerField(primary_key=True)
        status=models.CharField(max_length=50)
        error_message=models.CharField(max_length=50,null=True)

        class Meta:
             db_table='t_errors'

class Statusmodel(models.Model):
        status_id=models.AutoField(primary_key=True)
        status=models.CharField(max_length=15)

        class Meta:
             db_table='t_repair_status'



