from rest_framework import serializers
from .models import OrdenTrilla


class OrdenTrillaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenTrilla
        fields = '__all__'