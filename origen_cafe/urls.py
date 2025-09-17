from rest_framework.routers import DefaultRouter
from .viewsets import OrigenCafeViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'origen-cafe', OrigenCafeViewSet)

urlpatterns = [
	path('origen-cafe/listar/', views.listar_origen_cafe, name='origen_cafe_listar'),
	path('origen-cafe/nuevo/', views.add_origen_cafe, name='origen_cafe_nuevo'),
	path('origen-cafe/<int:pk>/editar/', views.edit_origen_cafe, name='origen_cafe_editar'),
	path('origen-cafe/<int:pk>/eliminar/', views.delete_origen_cafe, name='origen_cafe_eliminar'),
]

urlpatterns += router.urls