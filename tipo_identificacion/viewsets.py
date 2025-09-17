from rest_framework import viewsets
from .models import TipoIdentificacion
from .serializers import TipoIdentificacionSerializer
from core.mixins import OptimizedQuerysetMixin


class TipoIdentificacionViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = TipoIdentificacion.objects.all().order_by('tipo_identificacion')
    serializer_class = TipoIdentificacionSerializer