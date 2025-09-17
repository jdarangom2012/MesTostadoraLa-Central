from rest_framework import viewsets
from .models import SeleccionTueste
from .serializers import SeleccionTuesteSerializer
from core.mixins import OptimizedQuerysetMixin


class SeleccionTuesteViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = SeleccionTueste.objects.all().order_by('-fecha_ingreso')
    serializer_class = SeleccionTuesteSerializer