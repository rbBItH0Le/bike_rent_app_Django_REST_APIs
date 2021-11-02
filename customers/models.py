from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.



class Customodel(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    hashed_password=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    favorite_station_id=models.IntegerField()
    active_trip_id=models.IntegerField(null=True)
    credits=models.IntegerField(default=10)
    session_id=models.IntegerField(null=True)

    class Meta:
        db_table='t_customers'

class Custsessionmodel(models.Model):
    id=models.AutoField(primary_key=True)
    customer_id=models.IntegerField()
    access_token=models.CharField(max_length=200)

    class Meta:
        db_table='t_customer_sessions'


class Paymentmodel(models.Model):
    id=models.AutoField(primary_key=True)
    customer_id=models.IntegerField()
    trip_id=models.IntegerField(null=True)
    transaction_time=models.CharField(max_length=100)
    transaction_id=models.CharField(max_length=50)
    payment_method=models.CharField(max_length=20,default='credits')
    card_number=models.CharField(max_length=15,null=True)

    class Meta:
        db_table='t_payments'

