from rest_framework import serializers
from .models import OrdenSeleccionTostado


class OrdenSeleccionTostadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenSeleccionTostado
        fields = '__all__'
