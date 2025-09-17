from rest_framework import serializers
from .models import ZarandaGrupo


class ZarandaGrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZarandaGrupo
        fields = '__all__'