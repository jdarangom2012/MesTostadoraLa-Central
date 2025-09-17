from rest_framework import viewsets
from .models import CurvaTueste
from .serializers import CurvaTuesteSerializer


class CurvaTuesteViewSet(viewsets.ModelViewSet):
    queryset = CurvaTueste.objects.all()
    serializer_class = CurvaTuesteSerializer