from rest_framework import serializers
from cycles.models import Cyclemodel
from operators.models import Stationmodel
from operators.serialization import Erroralize

    
class Cyclenalize(serializers.ModelSerializer):
    class Meta:
        model=Cyclemodel
        fields=['cycle_id','station_id','category','is_charging','battery_percentage','model_number','status_id']

class Stationatrackalize(serializers.ModelSerializer):
    class Meta:
        model=Stationmodel
        fields=['location_lat','location_long']

class AddCycleSerializers(serializers.Serializer):
    response = Cyclenalize()
    status = Erroralize()

class ShowCycleSerializers(serializers.Serializer):
    response = Cyclenalize(many=True)
    status = Erroralize()

class Showgeorializers(serializers.Serializer):
    response=Stationatrackalize()
    status=Erroralize()
