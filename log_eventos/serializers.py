from rest_framework import serializers
from .models import LogEvento


class LogEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEvento
        fields = '__all__'
        read_only_fields = '__all__'