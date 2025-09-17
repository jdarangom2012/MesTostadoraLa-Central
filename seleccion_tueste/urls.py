from rest_framework.routers import DefaultRouter
from .viewsets import SeleccionTuesteViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'seleccion-tueste', SeleccionTuesteViewSet)

# Rutas HTML (popups)
urlpatterns = [
	path('ordenes-seleccion-tueste/listar/', views.listar_ordenes_seleccion_tueste, name='ordenes_seleccion_tueste_listar'),
	path('ordenes-seleccion-tueste/nuevo/', views.add_orden_seleccion_tueste, name='orden_seleccion_tueste_nuevo'),
	path('ordenes-seleccion-tueste/<int:pk>/editar/', views.edit_orden_seleccion_tueste, name='orden_seleccion_tueste_editar'),
	path('ordenes-seleccion-tueste/<int:pk>/eliminar/', views.delete_orden_seleccion_tueste, name='orden_seleccion_tueste_eliminar'),
]

# Rutas API
urlpatterns += router.urls