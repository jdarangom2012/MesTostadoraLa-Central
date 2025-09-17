from rest_framework import serializers
from .models import EstadoTarea


class EstadoTareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoTarea
        fields = '__all__'