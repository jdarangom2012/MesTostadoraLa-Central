from rest_framework.routers import DefaultRouter
from .viewsets import VariedadCafeViewSet

router = DefaultRouter()
router.register(r'variedad-cafe', VariedadCafeViewSet)

urlpatterns = router.urls