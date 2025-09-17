from rest_framework import viewsets
from .models import EstadoCliente
from .serializers import EstadoClienteSerializer
from core.mixins import OptimizedQuerysetMixin


class EstadoClienteViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = EstadoCliente.objects.all().order_by('estado_cliente')
    serializer_class = EstadoClienteSerializer