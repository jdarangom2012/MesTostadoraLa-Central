from rest_framework import viewsets
from .models import EstadoInvenCafe
from .serializers import EstadoInvenCafeSerializer
from core.mixins import OptimizedQuerysetMixin


class EstadoInvenCafeViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = EstadoInvenCafe.objects.all().order_by('estado_inven_cafe')
    serializer_class = EstadoInvenCafeSerializer