from rest_framework import viewsets, mixins
from .models import LogEvento
from .serializers import LogEventoSerializer
from core.mixins import OptimizedQuerysetMixin


class LogEventoViewSet(OptimizedQuerysetMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = LogEvento.objects.all().order_by('-fecha_utc')
    serializer_class = LogEventoSerializer