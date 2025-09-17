from rest_framework import serializers
from .models import EstadoCliente


class EstadoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCliente
        fields = '__all__'