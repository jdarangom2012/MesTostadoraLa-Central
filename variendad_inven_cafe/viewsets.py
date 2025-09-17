from rest_framework import viewsets
from .models import VariendadInvenCafe
from .serializers import VariendadInvenCafeSerializer
from core.mixins import OptimizedQuerysetMixin


class VariendadInvenCafeViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = VariendadInvenCafe.objects.all().order_by('variedad_inven_cafe')
    serializer_class = VariendadInvenCafeSerializer