from rest_framework import viewsets
from .models import Molienda
from .serializers import MoliendaSerializer
from core.mixins import OptimizedQuerysetMixin


class MoliendaViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = Molienda.objects.all().order_by('-fecha')
    serializer_class = MoliendaSerializer