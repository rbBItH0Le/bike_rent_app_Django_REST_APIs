from rest_framework import serializers
from cycles.models import Cyclemodel

class Cycserialize(serializers.ModelSerializer):
    class Meta:
        model=Cyclemodel
        fields='__all__'

