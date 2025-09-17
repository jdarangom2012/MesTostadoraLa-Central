from rest_framework import serializers
from .models import SeleccionTueste


class SeleccionTuesteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeleccionTueste
        fields = '__all__'