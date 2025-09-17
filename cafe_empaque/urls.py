from rest_framework.routers import DefaultRouter
from .viewsets import CafeEmpaqueViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'cafe-empaque', CafeEmpaqueViewSet)

urlpatterns = [
	path('empaque-cafe/listar/', views.listar_cafe_empaque, name='cafe_empaque_listar'),
	path('empaque-cafe/nuevo/', views.add_cafe_empaque, name='cafe_empaque_nuevo'),
	path('empaque-cafe/<int:pk>/editar/', views.edit_cafe_empaque, name='cafe_empaque_editar'),
	path('empaque-cafe/<int:pk>/eliminar/', views.delete_cafe_empaque, name='cafe_empaque_eliminar'),
]

urlpatterns += router.urls