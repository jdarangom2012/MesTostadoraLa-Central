from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .viewsets import InventarioCafeViewSet

html_urlpatterns = [
    path('inventario-cafe/listar/', views.listar_cafe, name='inventario_cafe_listar'),
    path('inventario-cafe/nuevo/', views.add_cafe, name='inventario_cafe_nuevo'),
    path('inventario-cafe/<int:pk>/editar/', views.edit_cafe, name='inventario_cafe_editar'),
    path('inventario-cafe/<int:pk>/eliminar/', views.delete_cafe, name='inventario_cafe_eliminar'),
]

router = DefaultRouter()
router.register(r'inventario-cafe', InventarioCafeViewSet)

urlpatterns = html_urlpatterns + [
    path('', include(router.urls)),
]