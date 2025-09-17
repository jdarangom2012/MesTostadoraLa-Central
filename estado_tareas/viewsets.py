from rest_framework import viewsets
from .models import EstadoTarea
from .serializers import EstadoTareaSerializer
from core.mixins import OptimizedQuerysetMixin


class EstadoTareaViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = EstadoTarea.objects.all().order_by('estado_tareas')
    serializer_class = EstadoTareaSerializer