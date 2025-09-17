from rest_framework.routers import DefaultRouter
from .viewsets import ProcesoInvenCafeViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'proceso-inven-cafe', ProcesoInvenCafeViewSet)

urlpatterns = [
	path('proceso-inven-cafe/listar/', views.listar_proceso_inven_cafe, name='proceso_inven_cafe_listar'),
	path('proceso-inven-cafe/nuevo/', views.add_proceso_inven_cafe, name='proceso_inven_cafe_nuevo'),
	path('proceso-inven-cafe/<int:pk>/editar/', views.edit_proceso_inven_cafe, name='proceso_inven_cafe_editar'),
	path('proceso-inven-cafe/<int:pk>/eliminar/', views.delete_proceso_inven_cafe, name='proceso_inven_cafe_eliminar'),
]

urlpatterns += router.urls