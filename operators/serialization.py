from rest_framework import serializers
from operators.models import Operatormodel,Operatsessionmodel

class Empserialize(serializers.ModelSerializer):
    class Meta:
        model=Operatormodel
        fields='__all__'

class Sesserialize(serializers.ModelSerializer):
    class Meta:
        model=Operatsessionmodel
        fields='__all__'
