from rest_framework import serializers
from .models import Molienda


class MoliendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Molienda
        fields = '__all__'