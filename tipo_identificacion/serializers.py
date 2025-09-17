from rest_framework import serializers
from .models import TipoIdentificacion


class TipoIdentificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoIdentificacion
        fields = '__all__'