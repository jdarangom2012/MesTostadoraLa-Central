from rest_framework import viewsets
from .models import NivelMolienda
from .serializers import NivelMoliendaSerializer
from core.mixins import OptimizedQuerysetMixin


class NivelMoliendaViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = NivelMolienda.objects.all().order_by('nivel_molienda')
    serializer_class = NivelMoliendaSerializer