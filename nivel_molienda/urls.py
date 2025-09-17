from rest_framework.routers import DefaultRouter
from .viewsets import NivelMoliendaViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'nivel-molienda', NivelMoliendaViewSet)

urlpatterns = [
	path('nivel-molienda/listar/', views.listar_niveles_molienda, name='nivel_molienda_listar'),
	path('nivel-molienda/nuevo/', views.add_nivel_molienda, name='nivel_molienda_nuevo'),
	path('nivel-molienda/<int:pk>/editar/', views.edit_nivel_molienda, name='nivel_molienda_editar'),
	path('nivel-molienda/<int:pk>/eliminar/', views.delete_nivel_molienda, name='nivel_molienda_eliminar'),
]

urlpatterns += router.urls