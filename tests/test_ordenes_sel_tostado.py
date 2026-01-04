from django.test import TestCase
from ordenes_seleccion_tostado.models import OrdenSeleccionTostado
from clientes.models import Cliente
from inventario_cafe.models import InventarioCafe
from empleados.models import Empleado
from estado_ordenes.models import EstadoOrden
from datetime import datetime, timedelta

class OrdenesSelTostadoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cliente = Cliente.objects.create(nombre='Cliente Test')
        cls.estado = EstadoOrden.objects.create(nombre='Estado Test')
        cls.empleado = Empleado.objects.create(nombres='Empleado', apellidos='Test')
        cls.cafe = InventarioCafe.objects.create(codigo='C-STOS-001')
        cls.ordenes = []
        for i in range(5):
            orden = OrdenSeleccionTostado.objects.create(
                cliente=cls.cliente,
                estado_orden=cls.estado,
                id_empleado=cls.empleado,
                id_inven_cafe=cls.cafe,
                fecha_ingreso=datetime.now(),
                fecha_inicio_orden=datetime.now() + timedelta(days=1),
                fecha_entrega=datetime.now() + timedelta(days=2),
                sacos_entero=2+i,
                peso_bruto=20.0+i,
                peso=18.0+i,
                prioridad=i+1
            )
            cls.ordenes.append(orden)

    def test_editar_ordenes(self):
        for i, orden in enumerate(self.ordenes[:4]):
            orden.sacos_entero += 1
            orden.save()
            self.assertEqual(OrdenSeleccionTostado.objects.get(pk=orden.pk).sacos_entero, 2+i+1)

    def test_eliminar_ordenes(self):
        for orden in self.ordenes[:2]:
            pk = orden.pk
            orden.delete()
            self.assertFalse(OrdenSeleccionTostado.objects.filter(pk=pk).exists())
