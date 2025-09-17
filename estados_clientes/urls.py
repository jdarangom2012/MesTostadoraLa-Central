from rest_framework.routers import DefaultRouter
from .viewsets import EstadoClienteViewSet

router = DefaultRouter()
router.register(r'estados-clientes', EstadoClienteViewSet)

urlpatterns = router.urls