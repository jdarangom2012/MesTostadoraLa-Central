from rest_framework import viewsets
from .models import TipoCliente
from .serializers import TipoClienteSerializer
from core.mixins import OptimizedQuerysetMixin


class TipoClienteViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = TipoCliente.objects.all().order_by('tipo_cliente')
    serializer_class = TipoClienteSerializer