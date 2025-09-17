from rest_framework.routers import DefaultRouter
from .viewsets import EstadoCafeViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'estado-cafe', EstadoCafeViewSet)

urlpatterns = [
	path('estado-cafe/listar/', views.listar_estado, name='estado_listar'),
	path('estado-cafe/nuevo/', views.add_estado, name='estado_nuevo'),
	path('estado-cafe/<int:pk>/editar/', views.edit_estado, name='estado_editar'),
	path('estado-cafe/<int:pk>/eliminar/', views.delete_estado, name='estado_eliminar'),
]

urlpatterns += router.urls