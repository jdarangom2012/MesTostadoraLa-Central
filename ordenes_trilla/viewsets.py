from rest_framework import viewsets
from .models import OrdenTrilla
from .serializers import OrdenTrillaSerializer
from core.mixins import OptimizedQuerysetMixin


class OrdenTrillaViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = OrdenTrilla.objects.all().order_by('-fecha_ingreso')
    serializer_class = OrdenTrillaSerializer
    select_related_fields = ['orden']