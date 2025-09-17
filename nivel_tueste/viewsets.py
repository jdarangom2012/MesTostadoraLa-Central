from rest_framework import viewsets
from .models import NivelTueste
from .serializers import NivelTuesteSerializer
from core.mixins import OptimizedQuerysetMixin


class NivelTuesteViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = NivelTueste.objects.all().order_by('nivel_tueste')
    serializer_class = NivelTuesteSerializer