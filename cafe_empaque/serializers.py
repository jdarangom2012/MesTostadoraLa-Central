from rest_framework import serializers
from .models import CafeEmpaque


class CafeEmpaqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeEmpaque
        fields = '__all__'