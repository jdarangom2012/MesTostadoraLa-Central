from rest_framework import viewsets
from .models import VariedadCafe
from .serializers import VariedadCafeSerializer
from core.mixins import OptimizedQuerysetMixin


class VariedadCafeViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = VariedadCafe.objects.all().order_by('variedad_cafe')
    serializer_class = VariedadCafeSerializer