from rest_framework.routers import DefaultRouter
from .viewsets import TamanoEmpaqueViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'tamano-empaque', TamanoEmpaqueViewSet)

# Importante: declarar primero las rutas HTML para que no las capture el router de DRF
urlpatterns = [
	path('tamano-empaque/listar/', views.listar_tamano_empaque, name='tamano_empaque_listar'),
	path('tamano-empaque/nuevo/', views.add_tamano_empaque, name='tamano_empaque_nuevo'),
	path('tamano-empaque/<int:pk>/editar/', views.edit_tamano_empaque, name='tamano_empaque_editar'),
	path('tamano-empaque/<int:pk>/eliminar/', views.delete_tamano_empaque, name='tamano_empaque_eliminar'),
] + router.urls