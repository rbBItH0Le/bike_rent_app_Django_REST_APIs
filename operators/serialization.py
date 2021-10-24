from rest_framework import serializers
from operators.models import Operatormodel,Operatsessionmodel, Stationmodel

class Empserialize(serializers.ModelSerializer):
    class Meta:
        model=Operatormodel
        fields='__all__'

class Sesserialize(serializers.ModelSerializer):
    class Meta:
        model=Operatsessionmodel
        fields='__all__'

class Stationalize(serializers.ModelSerializer):
    class Meta:
        model=Stationmodel
        fields=['id','operator_id','capacity','availability','address','post_code','location_lat','location_long','serialised_plan']