from django.urls import path
from rest_framework.routers import DefaultRouter
from .viewsets import MoliendaViewSet
from . import views

router = DefaultRouter()
router.register(r'molienda', MoliendaViewSet)

urlpatterns = [
	path('molienda/listar/', views.listar_molienda, name='molienda_listar'),
	path('molienda/nuevo/', views.add_molienda, name='molienda_nuevo'),
	path('molienda/<int:pk>/editar/', views.edit_molienda, name='molienda_editar'),
	path('molienda/<int:pk>/eliminar/', views.delete_molienda, name='molienda_eliminar'),
]

# Añadir rutas API sin sobrescribir las HTML
urlpatterns += router.urls