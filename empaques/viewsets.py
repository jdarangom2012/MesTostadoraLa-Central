from rest_framework import viewsets
from .models import Empaque
from .serializers import EmpaqueSerializer


class EmpaqueViewSet(viewsets.ModelViewSet):
    queryset = Empaque.objects.all()
    serializer_class = EmpaqueSerializer