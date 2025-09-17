from rest_framework.routers import DefaultRouter
from .viewsets import VariendadInvenCafeViewSet

router = DefaultRouter()
router.register(r'variendad-inven-cafe', VariendadInvenCafeViewSet)

urlpatterns = router.urls