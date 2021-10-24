from rest_framework import serializers
from managers.models import Managermodel
from operators.models import Operatormodel

class Managerialize(serializers.ModelSerializer):
    class Meta:
        model=Managermodel
        fields=['id','first_name','last_name','email','phone']

class Operationalize(serializers.ModelSerializer):
    class Meta:
        model=Operatormodel
        fields=['id','first_name','last_name','email','phone','session_id']
