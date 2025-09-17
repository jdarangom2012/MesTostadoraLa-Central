from rest_framework import serializers
from .models import Tueste


class TuesteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tueste
        fields = '__all__'