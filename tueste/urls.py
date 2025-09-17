from rest_framework.routers import DefaultRouter
from .viewsets import TuesteViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'tueste', TuesteViewSet)

# Rutas HTML (popups) primero
urlpatterns = [
	path('ordenes-tueste/listar/', views.listar_ordenes_tueste, name='ordenes_tueste_listar'),
	path('ordenes-tueste/nuevo/', views.add_orden_tueste, name='orden_tueste_nuevo'),
	path('ordenes-tueste/<int:pk>/editar/', views.edit_orden_tueste, name='orden_tueste_editar'),
	path('ordenes-tueste/<int:pk>/eliminar/', views.delete_orden_tueste, name='orden_tueste_eliminar'),
]

# Rutas API
urlpatterns += router.urls