from rest_framework import serializers
from .models import VariedadCafe


class VariedadCafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariedadCafe
        fields = '__all__'