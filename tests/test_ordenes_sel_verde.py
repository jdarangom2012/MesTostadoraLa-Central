from django.test import TestCase
from ordenes_seleccion_verde.models import OrdenSeleccionVerde
from clientes.models import Cliente
from inventario_cafe.models import InventarioCafe
from empleados.models import Empleado
from estado_ordenes.models import EstadoOrden
from datetime import datetime, timedelta

class OrdenesSelVerdeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cliente = Cliente.objects.create(nombre='Cliente Test')
        cls.estado = EstadoOrden.objects.create(nombre='Estado Test')
        cls.empleado = Empleado.objects.create(nombres='Empleado', apellidos='Test')
        cls.cafe = InventarioCafe.objects.create(codigo='C-SVER-001')
        cls.ordenes = []
        for i in range(5):
            orden = OrdenSeleccionVerde.objects.create(
                cliente=cls.cliente,
                estado_orden=cls.estado,
                id_empleado=cls.empleado,
                id_inven_cafe=cls.cafe,
                fecha_ingreso=datetime.now(),
                fecha_inicio_orden=datetime.now() + timedelta(days=1),
                fecha_entrega=datetime.now() + timedelta(days=2),
                sacos_entero=4+i,
                peso_bruto=40.0+i,
                peso=36.0+i,
                prioridad=i+1
            )
            cls.ordenes.append(orden)

    def test_editar_ordenes(self):
        for i, orden in enumerate(self.ordenes[:4]):
            orden.estado_orden = self.estado
            orden.save()
            self.assertEqual(OrdenSeleccionVerde.objects.get(pk=orden.pk).estado_orden, self.estado)

    def test_eliminar_ordenes(self):
        for orden in self.ordenes[:2]:
            pk = orden.pk
            orden.delete()
            self.assertFalse(OrdenSeleccionVerde.objects.filter(pk=pk).exists())
