from rest_framework import serializers
from managers.models import Managermodel,Managessionmodel
from operators.models import Operatormodel
from operators.serialization import Erroralize

class Managerialize(serializers.ModelSerializer):
    class Meta:
        model=Managermodel
        fields=['id','first_name','last_name','email','phone']

class Managesessionalize(serializers.ModelSerializer):
    class Meta:
        model=Managessionmodel
        fields=['id','manager_id','access_token']

class Operationalize(serializers.ModelSerializer):
    class Meta:
        model=Operatormodel
        fields=['id','first_name','last_name','email','phone','session_id']

class Onboardanlize(serializers.Serializer):
    response=Operationalize()
    status=Erroralize()

class Loginalize(serializers.Serializer):
    response=Managesessionalize()
    status=Erroralize()

class Managesignalize(serializers.Serializer):
    response=Managerialize()
    status=Erroralize()