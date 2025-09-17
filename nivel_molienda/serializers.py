from rest_framework import serializers
from .models import NivelMolienda


class NivelMoliendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NivelMolienda
        fields = '__all__'