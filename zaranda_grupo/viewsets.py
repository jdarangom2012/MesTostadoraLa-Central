from rest_framework import viewsets
from .models import ZarandaGrupo
from .serializers import ZarandaGrupoSerializer
from core.mixins import OptimizedQuerysetMixin


class ZarandaGrupoViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = ZarandaGrupo.objects.all().order_by('zaranda_grupo')
    serializer_class = ZarandaGrupoSerializer