from rest_framework import viewsets
from .models import TamanoEmpaque
from .serializers import TamanoEmpaqueSerializer
from core.mixins import OptimizedQuerysetMixin


class TamanoEmpaqueViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = TamanoEmpaque.objects.all().order_by('tamano_empaque')
    serializer_class = TamanoEmpaqueSerializer