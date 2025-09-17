from rest_framework import serializers
from .models import EstadoInvenCafe


class EstadoInvenCafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoInvenCafe
        fields = '__all__'