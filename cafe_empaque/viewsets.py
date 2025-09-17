from rest_framework import viewsets
from .models import CafeEmpaque
from .serializers import CafeEmpaqueSerializer
from core.mixins import OptimizedQuerysetMixin


class CafeEmpaqueViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = CafeEmpaque.objects.all().order_by('empaque_cafe')
    serializer_class = CafeEmpaqueSerializer