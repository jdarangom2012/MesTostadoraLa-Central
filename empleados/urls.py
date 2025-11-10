from django.urls import path
from .views import listar_empleados, add_empleado, detail_empleado, delete_empleado

urlpatterns = [
    path('empleados/', listar_empleados, name='listar_empleados'),
    path('empleados/nuevo/', add_empleado, name='add_empleado'),
    path('empleados/<int:id>/editar/', detail_empleado, name='detail_empleado'),
    path('empleados/<int:id>/eliminar/', delete_empleado, name='delete_empleado'),
]
