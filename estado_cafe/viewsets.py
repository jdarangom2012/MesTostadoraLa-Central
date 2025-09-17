from rest_framework import viewsets
from .models import EstadoCafe
from .serializers import EstadoCafeSerializer
from core.mixins import OptimizedQuerysetMixin


class EstadoCafeViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = EstadoCafe.objects.all().order_by('estado_cafe')
    serializer_class = EstadoCafeSerializer