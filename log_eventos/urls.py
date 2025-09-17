from rest_framework.routers import DefaultRouter
from .viewsets import LogEventoViewSet

router = DefaultRouter()
router.register(r'log-eventos', LogEventoViewSet)

urlpatterns = router.urls