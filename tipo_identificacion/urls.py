from rest_framework.routers import DefaultRouter
from .viewsets import TipoIdentificacionViewSet

router = DefaultRouter()
router.register(r'tipo-identificacion', TipoIdentificacionViewSet)

urlpatterns = router.urls