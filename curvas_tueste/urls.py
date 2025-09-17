from django.urls import path
from rest_framework.routers import DefaultRouter
from .viewsets import CurvaTuesteViewSet
from . import views

router = DefaultRouter()
router.register(r'curvas-tueste', CurvaTuesteViewSet)

urlpatterns = [
	# HTML modal routes (con prefijo)
	path('curvas_tueste/', views.listar_curvas_tueste, name='curvas_tueste_listar'),
	path('curvas_tueste/nuevo/', views.add_curva_tueste, name='curvas_tueste_nuevo'),
	path('curvas_tueste/<int:pk>/editar/', views.edit_curva_tueste, name='curvas_tueste_editar'),
	path('curvas_tueste/<int:pk>/eliminar/', views.delete_curva_tueste, name='curvas_tueste_eliminar'),
]

# API routes (se exponen bajo /api/v1/ desde mes_central.urls)
urlpatterns += router.urls