from rest_framework.routers import DefaultRouter
from .viewsets import ClienteViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)

# 1) Rutas HTML primero para que no las capture el router ("listar" antes que detalle API)
urlpatterns = [
	path('clientes/listar/', views.listar_clientes, name='clientes_listar'),
	path('clientes/nuevo/', views.add_cliente, name='cliente_nuevo'),
	path('clientes/<int:pk>/editar/', views.edit_cliente, name='cliente_editar'),
	path('clientes/<int:pk>/eliminar/', views.delete_cliente, name='cliente_eliminar'),
]

# 2) Rutas API (también estarán disponibles bajo /api/v1/ desde mes_central.urls)
urlpatterns += router.urls
