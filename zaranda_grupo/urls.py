from rest_framework.routers import DefaultRouter
from .viewsets import ZarandaGrupoViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'zaranda-grupo', ZarandaGrupoViewSet)

urlpatterns = [
	path('zaranda-grupo/listar/', views.listar_zaranda_grupo, name='zaranda_grupo_listar'),
	path('zaranda-grupo/nuevo/', views.add_zaranda_grupo, name='zaranda_grupo_nuevo'),
	path('zaranda-grupo/<int:pk>/editar/', views.edit_zaranda_grupo, name='zaranda_grupo_editar'),
	path('zaranda-grupo/<int:pk>/eliminar/', views.delete_zaranda_grupo, name='zaranda_grupo_eliminar'),
]

urlpatterns += router.urls