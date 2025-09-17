from rest_framework.routers import DefaultRouter
from .viewsets import EstadoInvenCafeViewSet

router = DefaultRouter()
router.register(r'estado-inven-cafe', EstadoInvenCafeViewSet)

urlpatterns = router.urls