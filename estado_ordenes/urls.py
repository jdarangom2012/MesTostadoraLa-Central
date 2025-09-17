from rest_framework.routers import DefaultRouter
from .viewsets import EstadoOrdenViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'estado-ordenes', EstadoOrdenViewSet)

urlpatterns = [
	path('estado-orden/listar/', views.listar_estado_orden, name='estado_orden_listar'),
	path('estado-orden/nuevo/', views.add_estado_orden, name='estado_orden_nuevo'),
	path('estado-orden/<int:pk>/editar/', views.edit_estado_orden, name='estado_orden_editar'),
	path('estado-orden/<int:pk>/eliminar/', views.delete_estado_orden, name='estado_orden_eliminar'),
]

urlpatterns += router.urls