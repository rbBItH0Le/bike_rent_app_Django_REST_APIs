from rest_framework import serializers
from customers.models import Customodel,Paymentmodel

class Custserialize(serializers.ModelSerializer):
    class Meta:
        model=Customodel
        fields='__all__'

class Payerialize(serializers.ModelSerializer):
    class Meta:
        model=Paymentmodel
        fields=['id','customer_id','transaction_id','payment_method','card_number']


