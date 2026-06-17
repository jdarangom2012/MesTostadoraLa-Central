from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views
from .viewsets import VariendadInvenCafeViewSet

router = DefaultRouter()
router.register(r'variendad-inven-cafe', VariendadInvenCafeViewSet)

urlpatterns = [
	path('variedad-inven-cafe/listar/', views.listar_variedad_inven_cafe, name='variedad_inven_cafe_listar'),
	path('variedad-inven-cafe/nuevo/', views.add_variedad_inven_cafe, name='variedad_inven_cafe_nuevo'),
	path('variedad-inven-cafe/<int:pk>/editar/', views.edit_variedad_inven_cafe, name='variedad_inven_cafe_editar'),
	path('variedad-inven-cafe/<int:pk>/eliminar/', views.delete_variedad_inven_cafe, name='variedad_inven_cafe_eliminar'),
]

urlpatterns += router.urls