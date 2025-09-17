from rest_framework import serializers
from .models import ProcesoInvenCafe


class ProcesoInvenCafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcesoInvenCafe
        fields = '__all__'