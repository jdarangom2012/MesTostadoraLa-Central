from rest_framework import serializers
from .models import OrdenSeleccionVerde


class OrdenSeleccionVerdeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenSeleccionVerde
        fields = '__all__'