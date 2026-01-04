from django.test import TestCase
from ordenes.models import Orden
from clientes.models import Cliente
from inventario_cafe.models import InventarioCafe
from empleados.models import Empleado
from estado_ordenes.models import EstadoOrden
from datetime import datetime, timedelta

class OrdenesProduccionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cliente = Cliente.objects.create(nombre='Cliente Test')
        cls.estado = EstadoOrden.objects.create(nombre='Estado Test')
        cls.empleado = Empleado.objects.create(nombres='Empleado', apellidos='Test')
        cls.cafe = InventarioCafe.objects.create(codigo='C-001')
        cls.ordenes = []
        for i in range(5):
            orden = Orden.objects.create(
                cliente=cls.cliente,
                estado_orden=cls.estado,
                id_empleado=cls.empleado,
                id_inven_cafe=cls.cafe,
                orden=f'ORD-{i+1}',
                fecha_ingreso=datetime.now(),
                fecha_inicio_orden=datetime.now() + timedelta(days=1),
                fecha_entrega=datetime.now() + timedelta(days=2),
                sacos_entero=10+i,
                peso_bruto=100.0+i,
                peso=90.0+i,
                trabajo_empaque=True,
                etiqueta_invima=False,
                prioridad=i+1
            )
            cls.ordenes.append(orden)

    def test_editar_ordenes(self):
        for i, orden in enumerate(self.ordenes[:4]):
            orden.peso_bruto += 10
            orden.save()
            self.assertEqual(Orden.objects.get(pk=orden.pk).peso_bruto, 100.0+i+10)

    def test_eliminar_ordenes(self):
        for orden in self.ordenes[:2]:
            pk = orden.pk
            orden.delete()
            self.assertFalse(Orden.objects.filter(pk=pk).exists())
