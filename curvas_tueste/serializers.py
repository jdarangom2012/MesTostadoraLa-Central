from rest_framework import serializers
from .models import CurvaTueste


class CurvaTuesteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurvaTueste
        fields = '__all__'