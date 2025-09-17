from django.urls import path
from . import views

urlpatterns = [
    path('empaque/listar/', views.listar_empaque, name='empaque_listar'),
    path('empaque/nuevo/', views.add_empaque, name='empaque_nuevo'),
    path('empaque/<int:pk>/editar/', views.edit_empaque, name='empaque_editar'),
    path('empaque/<int:pk>/eliminar/', views.delete_empaque, name='empaque_eliminar'),
]
from rest_framework.routers import DefaultRouter
from .viewsets import EmpaqueViewSet

router = DefaultRouter()
router.register(r'empaques', EmpaqueViewSet)

# Append router URLs instead of overwriting custom paths
urlpatterns += router.urls