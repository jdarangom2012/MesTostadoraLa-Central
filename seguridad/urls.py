from django.urls import path

from . import views

urlpatterns = [
    path('roles/', views.roles_listar, name='seguridad_roles_listar'),
    path('roles/nuevo/', views.roles_crear, name='seguridad_roles_crear'),
    path('roles/<int:pk>/editar/', views.roles_editar, name='seguridad_roles_editar'),
    path('roles/<int:pk>/eliminar/', views.roles_eliminar, name='seguridad_roles_eliminar'),

    path('permisos/', views.permisos_listar, name='seguridad_permisos_listar'),
    path('permisos/nuevo/', views.permisos_crear, name='seguridad_permisos_crear'),
    path('permisos/<int:pk>/editar/', views.permisos_editar, name='seguridad_permisos_editar'),
    path('permisos/<int:pk>/eliminar/', views.permisos_eliminar, name='seguridad_permisos_eliminar'),

    path('modulos/', views.modulos_listar, name='seguridad_modulos_listar'),
    path('modulos/nuevo/', views.modulos_crear, name='seguridad_modulos_crear'),
    path('modulos/<int:pk>/editar/', views.modulos_editar, name='seguridad_modulos_editar'),
    path('modulos/<int:pk>/eliminar/', views.modulos_eliminar, name='seguridad_modulos_eliminar'),

    path('permisos-campo/', views.permisos_campo_listar, name='seguridad_permisos_campo_listar'),
    path('permisos-campo/nuevo/', views.permisos_campo_crear, name='seguridad_permisos_campo_crear'),
    path('permisos-campo/<int:pk>/editar/', views.permisos_campo_editar, name='seguridad_permisos_campo_editar'),
    path('permisos-campo/<int:pk>/eliminar/', views.permisos_campo_eliminar, name='seguridad_permisos_campo_eliminar'),

    path('gestionar-permisos/', views.gestionar_permisos, name='seguridad_gestionar_permisos'),
]
