from rest_framework.routers import DefaultRouter
from .viewsets import NivelTuesteViewSet

router = DefaultRouter()
router.register(r'nivel-tueste', NivelTuesteViewSet)

urlpatterns = router.urls