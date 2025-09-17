from rest_framework.routers import DefaultRouter
from .viewsets import TipoClienteViewSet

router = DefaultRouter()
router.register(r'tipo-clientes', TipoClienteViewSet)

urlpatterns = router.urls