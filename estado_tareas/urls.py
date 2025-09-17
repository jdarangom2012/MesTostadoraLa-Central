from rest_framework.routers import DefaultRouter
from .viewsets import EstadoTareaViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'estado-tareas', EstadoTareaViewSet)

urlpatterns = [
	path('estado-tareas/listar/', views.listar_estado_tareas, name='estado_tareas_listar'),
	path('estado-tareas/nuevo/', views.add_estado_tareas, name='estado_tareas_nuevo'),
	path('estado-tareas/<int:pk>/editar/', views.edit_estado_tareas, name='estado_tareas_editar'),
	path('estado-tareas/<int:pk>/eliminar/', views.delete_estado_tareas, name='estado_tareas_eliminar'),
]

urlpatterns += router.urls