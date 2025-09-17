from rest_framework.routers import DefaultRouter
from .viewsets import MaterialViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'materiales', MaterialViewSet)

# HTML first
urlpatterns = [
	path('materiales/listar/', views.listar_materiales, name='materiales_listar'),
	path('materiales/nuevo/', views.add_material, name='material_nuevo'),
	path('materiales/<int:pk>/editar/', views.edit_material, name='material_editar'),
	path('materiales/<int:pk>/eliminar/', views.delete_material, name='material_eliminar'),
]

urlpatterns += router.urls