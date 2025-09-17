from rest_framework import viewsets
from .models import OrigenCafe
from .serializers import OrigenCafeSerializer
from core.mixins import OptimizedQuerysetMixin


class OrigenCafeViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = OrigenCafe.objects.all().order_by('origen')
    serializer_class = OrigenCafeSerializer