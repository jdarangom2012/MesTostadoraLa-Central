from rest_framework import serializers
from .models import EstadoOrden


class EstadoOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoOrden
        fields = '__all__'