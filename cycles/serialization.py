from rest_framework import serializers
from operators.models import Cyclemodel

class Cycserialize(serializers.ModelSerializer):
    class Meta:
        model=Cyclemodel
        fields='__all__'

