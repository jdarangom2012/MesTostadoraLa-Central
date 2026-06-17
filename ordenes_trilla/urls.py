from rest_framework.routers import DefaultRouter
from .viewsets import OrdenTrillaViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'ordenes-trilla', OrdenTrillaViewSet)

# Rutas HTML (popups) primero
urlpatterns = [
	path('ordenes-trilla/listar/', views.listar_ordenes_trilla, name='ordenes_trilla_listar'),
	path('ordenes-trilla/nuevo/', views.add_orden_trilla, name='orden_trilla_nuevo'),
	path('ordenes-trilla/defaults/', views.orden_trilla_defaults, name='orden_trilla_defaults'),
	path('ordenes-trilla/<int:pk>/editar/', views.edit_orden_trilla, name='orden_trilla_editar'),
	path('ordenes-trilla/<int:pk>/eliminar/', views.delete_orden_trilla, name='orden_trilla_eliminar'),
]

# Rutas API
urlpatterns += router.urls