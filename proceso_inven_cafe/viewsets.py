from rest_framework import viewsets
from .models import ProcesoInvenCafe
from .serializers import ProcesoInvenCafeSerializer
from core.mixins import OptimizedQuerysetMixin


class ProcesoInvenCafeViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = ProcesoInvenCafe.objects.all().order_by('proceso_inven_cafe')
    serializer_class = ProcesoInvenCafeSerializer