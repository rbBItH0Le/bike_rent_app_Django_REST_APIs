from rest_framework import serializers
from cycles.models import Cyclemodel
from operators.serialization import Erroralize

    
class Cyclenalize(serializers.ModelSerializer):
    class Meta:
        model=Cyclemodel
        fields=['cycle_id','station_id','category','is_charging','battery_percentage','model_number','status_id']

class AddCycleSerializers(serializers.Serializer):
    response = Cyclenalize()
    status = Erroralize()

class ShowCycleSerializers(serializers.Serializer):
    response = Cyclenalize(many=True)
    status = Erroralize()
