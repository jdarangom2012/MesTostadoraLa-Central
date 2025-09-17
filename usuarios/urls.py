from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_usuarios, name='usuarios_listar'),
]
