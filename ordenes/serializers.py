from rest_framework import serializers
from .models import Orden
from tueste.models import Tueste
from molienda.models import Molienda
from ordenes_trilla.models import OrdenTrilla
from ordenes_seleccion_verde.models import OrdenSeleccionVerde


class OrdenTuesteMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tueste
        fields = ['id', 'fecha_ingreso', 'rendimiento', 'nivel_tueste']


class OrdenMoliendaMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Molienda
        fields = ['id', 'fecha', 'peso_moler', 'nivel_molienda']


class OrdenTrillaMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenTrilla
        fields = ['id', 'fecha_ingreso', 'rendimiento', 'peso_cafe_bruto', 'peso_cafe_verde']


class OrdenSeleccionVerdeMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenSeleccionVerde
        fields = ['id', 'fecha_ingreso', 'peso_aceptado', 'humedad', 'densidad']


class OrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = '__all__'


class OrdenDetailSerializer(OrdenSerializer):
    tuestes = OrdenTuesteMiniSerializer(source='tueste_set', many=True, read_only=True)
    moliendas = OrdenMoliendaMiniSerializer(source='molienda_set', many=True, read_only=True)
    trillas = OrdenTrillaMiniSerializer(source='ordentrilla_set', many=True, read_only=True)
    seleccion_verde = OrdenSeleccionVerdeMiniSerializer(source='ordenseleccionverde_set', many=True, read_only=True)
    kpis = serializers.DictField(read_only=True)

    class Meta(OrdenSerializer.Meta):
        # When base uses '__all__', we must redefine explicitly
        model = Orden
        fields = '__all__'