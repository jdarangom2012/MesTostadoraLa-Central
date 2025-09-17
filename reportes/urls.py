from django.urls import path
from . import views

urlpatterns = [
    path('reportes/ordenes-por-estado/', views.OrdenesPorEstadoView.as_view()),
    path('reportes/inventario-resumen/', views.InventarioResumenView.as_view()),
    path('reportes/rendimiento-tueste/', views.RendimientoTuesteView.as_view()),
    path('reportes/produccion-diaria/', views.ProduccionDiariaView.as_view()),
    path('reportes/kpis-resumen/', views.KPIsResumenView.as_view()),
]