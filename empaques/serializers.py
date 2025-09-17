from rest_framework import serializers
from .models import Empaque


class EmpaqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empaque
        fields = '__all__'