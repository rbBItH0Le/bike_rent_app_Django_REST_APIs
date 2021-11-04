from rest_framework import serializers
from customers.models import Customodel, Custsessionmodel,Paymentmodel
from operators.serialization import Erroralize

class Custserialize(serializers.ModelSerializer):
    class Meta:
        model=Customodel
        fields='__all__'

class Custosessionalize(serializers.ModelSerializer):
    class Meta:
        model=Custsessionmodel
        fields='__all__'

class Payerialize(serializers.ModelSerializer):
    class Meta:
        model=Paymentmodel
        fields=['id','customer_id','transaction_id','payment_method','card_number', 'charge']

class Singupalize(serializers.Serializer):
    response=Custserialize()
    status=Erroralize()

class Custloginalize(serializers.Serializer):
    response=Custosessionalize()
    status=Erroralize()

class PaymentResponseSerialiser(serializers.Serializer):
    response=Payerialize()
    status=Erroralize


