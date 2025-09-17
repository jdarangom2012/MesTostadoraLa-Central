from rest_framework import viewsets
from .models import Material
from .serializers import MaterialSerializer
from core.mixins import OptimizedQuerysetMixin


class MaterialViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = Material.objects.all().order_by('descripcion')
    serializer_class = MaterialSerializer