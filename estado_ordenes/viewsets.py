from rest_framework import viewsets
from .models import EstadoOrden
from .serializers import EstadoOrdenSerializer
from core.mixins import OptimizedQuerysetMixin


class EstadoOrdenViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = EstadoOrden.objects.all().order_by('estado_orden')
    serializer_class = EstadoOrdenSerializer