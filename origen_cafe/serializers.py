from rest_framework import serializers
from .models import OrigenCafe


class OrigenCafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrigenCafe
        fields = '__all__'