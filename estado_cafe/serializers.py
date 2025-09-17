from rest_framework import serializers
from .models import EstadoCafe


class EstadoCafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCafe
        fields = '__all__'