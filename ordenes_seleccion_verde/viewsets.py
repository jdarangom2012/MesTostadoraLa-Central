from rest_framework import viewsets
from .models import OrdenSeleccionVerde
from .serializers import OrdenSeleccionVerdeSerializer
from core.mixins import OptimizedQuerysetMixin


class OrdenSeleccionVerdeViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = OrdenSeleccionVerde.objects.all().order_by('-fecha_ingreso')
    serializer_class = OrdenSeleccionVerdeSerializer