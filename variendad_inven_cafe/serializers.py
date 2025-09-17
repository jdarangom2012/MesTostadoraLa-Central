from rest_framework import serializers
from .models import VariendadInvenCafe


class VariendadInvenCafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariendadInvenCafe
        fields = '__all__'