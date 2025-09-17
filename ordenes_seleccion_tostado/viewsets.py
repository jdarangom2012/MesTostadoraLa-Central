from rest_framework import viewsets
from .models import OrdenSeleccionTostado
from .serializers import OrdenSeleccionTostadoSerializer


class OrdenSeleccionTostadoViewSet(viewsets.ModelViewSet):
    queryset = OrdenSeleccionTostado.objects.all().order_by('-fecha_ingreso', '-id')
    serializer_class = OrdenSeleccionTostadoSerializer
