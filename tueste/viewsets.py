from rest_framework import viewsets
from .models import Tueste
from .serializers import TuesteSerializer
from core.mixins import OptimizedQuerysetMixin


class TuesteViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = Tueste.objects.all().order_by('-fecha_ingreso')
    serializer_class = TuesteSerializer