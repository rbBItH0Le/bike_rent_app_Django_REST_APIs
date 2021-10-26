from rest_framework import serializers
from operators.models import Cyclemodel, Errormodel, Statusmodel
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
        fields=['station_id','capacity','availability','address','post_code','location_lat','location_long','serialised_plan']

class Cyclenalize(serializers.ModelSerializer):
    class Meta:
        model=Cyclemodel
        fields=['cycle_id','station_id','category','is_charging','battery_percentage','model_number','status_id']

class Erroralize(serializers.ModelSerializer):
    class Meta:
        model=Errormodel
        fields='__all__'

class Statusalize(serializers.ModelSerializer):
    class Meta:
        model=Statusmodel
        fields='__all__'

class FiltersSerializers(serializers.Serializer):
    response = Empserialize()
    status = Erroralize()

class LoginSerializers(serializers.Serializer):
    response = Sesserialize()
    status = Erroralize()

class AddstatSerializers(serializers.Serializer):
    response = Stationalize()
    status = Erroralize()

class ShowstatSerializers(serializers.Serializer):
    response = Stationalize(many=True)
    status = Erroralize()
   
class AddCycleSerializers(serializers.Serializer):
    response = Cyclenalize()
    status = Erroralize()

class ShowCycleSerializers(serializers.Serializer):
    response = Cyclenalize(many=True)
    status = Erroralize()

class ShowCycleStatusSerializers(serializers.Serializer):
    response = Statusalize(many=True)
    status = Erroralize()