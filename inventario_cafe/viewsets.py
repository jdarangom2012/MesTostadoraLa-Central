from rest_framework import viewsets
from .models import InventarioCafe
from .serializers import InventarioCafeSerializer
from core.mixins import OptimizedQuerysetMixin


class InventarioCafeViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = InventarioCafe.objects.all().order_by('-fecha_ingreso')
    serializer_class = InventarioCafeSerializer
    select_related_fields = ['cliente', 'estado_cafe', 'empaquecafe']