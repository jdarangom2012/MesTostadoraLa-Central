from rest_framework.routers import DefaultRouter
from .viewsets import OrdenSeleccionTostadoViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'ordenes-seleccion-tostado', OrdenSeleccionTostadoViewSet)

urlpatterns = [
	path('ordenes-seleccion-tostado/listar/', views.listar_ordenes_seleccion_tostado, name='ordenes_seleccion_tostado_listar'),
	path('ordenes-seleccion-tostado/nuevo/', views.add_orden_seleccion_tostado, name='orden_seleccion_tostado_nuevo'),
	path('ordenes-seleccion-tostado/defaults/', views.orden_seleccion_tostado_defaults, name='orden_seleccion_tostado_defaults'),
	path('ordenes-seleccion-tostado/<int:pk>/editar/', views.edit_orden_seleccion_tostado, name='orden_seleccion_tostado_editar'),
	path('ordenes-seleccion-tostado/<int:pk>/eliminar/', views.delete_orden_seleccion_tostado, name='orden_seleccion_tostado_eliminar'),
]

urlpatterns += router.urls