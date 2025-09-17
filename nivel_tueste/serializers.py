from rest_framework import serializers
from .models import NivelTueste


class NivelTuesteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NivelTueste
        fields = '__all__'