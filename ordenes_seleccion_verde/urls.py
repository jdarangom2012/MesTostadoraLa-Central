from rest_framework.routers import DefaultRouter
from .viewsets import OrdenSeleccionVerdeViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'ordenes-seleccion-verde', OrdenSeleccionVerdeViewSet)

urlpatterns = [
	path('ordenes-seleccion-verde/listar/', views.listar_ordenes_seleccion_verde, name='ordenes_seleccion_verde_listar'),
	path('ordenes-seleccion-verde/nuevo/', views.add_orden_seleccion_verde, name='orden_seleccion_verde_nuevo'),
	path('ordenes-seleccion-verde/<int:pk>/editar/', views.edit_orden_seleccion_verde, name='orden_seleccion_verde_editar'),
	path('ordenes-seleccion-verde/<int:pk>/eliminar/', views.delete_orden_seleccion_verde, name='orden_seleccion_verde_eliminar'),
]

urlpatterns += router.urls