from rest_framework import serializers
from .models import TamanoEmpaque


class TamanoEmpaqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TamanoEmpaque
        fields = '__all__'