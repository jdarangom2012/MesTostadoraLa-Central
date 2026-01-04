from django.conf import settings
import pytest
@pytest.mark.django_db(transaction=True)
def test_bulk_crud_sqlserver():
    """
    Prueba CRUD completa contra SQL Server: crea, edita y elimina 3 órdenes.
    Verifica que no haya errores y que los cambios se reflejen.
    """
    from clientes.models import Cliente
    from estado_ordenes.models import EstadoOrden
    from empleados.models import Empleado
    from ordenes.models import Orden
    from django.utils import timezone

    # Asegura datos referenciales
    cliente, _ = Cliente.objects.get_or_create(nombre='Cliente Test', defaults={'apellidos': 'Test', 'created_at': timezone.now()})
    estado, _ = EstadoOrden.objects.get_or_create(estado_orden='En Espera')
    empleado = Empleado.objects.first()
    if not empleado:
        empleado = Empleado.objects.create(
            identificacion='9999', nombres='Empleado', apellidos='Test', estado='Activo', fecha_ingreso=timezone.now()
        )

    # Crear 3 órdenes
    ids = []
    for i in range(3):
        o = Orden.objects.create(
            cliente=cliente,
            estado_orden=estado,
            id_empleado=empleado,
            orden=f'ORDSQL{i+1}',
            fecha_ingreso=timezone.now(),
            fecha_inicio_orden=timezone.now(),
            prioridad=1,
        )
        ids.append(o.id)
    assert Orden.objects.filter(id__in=ids).count() == 3

    # Editar cada una
    for oid in ids:
        o = Orden.objects.get(id=oid)
        o.orden = f'EDITSQL{oid}'
        o.prioridad = 2
        o.save()
        o.refresh_from_db()
        assert o.orden.startswith('EDITSQL')
        assert o.prioridad == 2

    # Eliminar todas
    for oid in ids:
        Orden.objects.filter(id=oid).delete()
    assert Orden.objects.filter(id__in=ids).count() == 0
from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from .models import Orden
from clientes.models import Cliente

class OrdenTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nombre="Cliente Test")
        from estado_ordenes.models import EstadoOrden
        self.estado_orden = EstadoOrden.objects.create(estado_orden="Pendiente")
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        from django.contrib.auth.models import Permission
        perms = Permission.objects.filter(codename__in=['add_orden', 'change_orden', 'view_orden', 'delete_orden'])
        self.user.user_permissions.set(perms)

    def test_creacion_orden_con_campo_orden(self):
        url = reverse('ordenes_produccion_nuevo')
        data = {
            'cliente': self.cliente.id,
            'orden': 'ORD00001',
                'estado_orden': self.estado_orden.id,
                'estado_inven_cafe': '',
            'fecha_orden': '',
            'fecha_entrega': '',
            'notas': 'Prueba',
            'trilla': False,
            'selec_cafe_verde': False,
            'tueste_flag': False,
            'selec_cafe_tostado': False,
            'molienda_flag': False,
            'empaque_flag': False,
            'conf_trilla': False,
            'conf_sel_verde': False,
            'conf_tueste': False,
            'conf_sel_tostado': False,
            'conf_molienda': False,
            'conf_empaque': False,
            'prioridad': 1,
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        orden = Orden.objects.latest('id')
        self.assertEqual(orden.orden, 'ORD00001')

    def test_edicion_orden_modifica_campo_orden(self):
        from django.utils import timezone
        orden = Orden.objects.create(cliente=self.cliente, orden='ORD00002', estado_orden=self.estado_orden, created_at=timezone.now())
        url = reverse('ordenes_produccion_editar', args=[orden.id])
        data = {
            'cliente': self.cliente.id,
            'orden': 'ORD00099',
                'estado_orden': self.estado_orden.id,
                'estado_inven_cafe': '',
            'fecha_orden': '',
            'fecha_entrega': '',
            'notas': 'Editada',
            'trilla': False,
            'selec_cafe_verde': False,
            'tueste_flag': False,
            'selec_cafe_tostado': False,
            'molienda_flag': False,
            'empaque_flag': False,
            'conf_trilla': False,
            'conf_sel_verde': False,
            'conf_tueste': False,
            'conf_sel_tostado': False,
            'conf_molienda': False,
            'conf_empaque': False,
            'prioridad': 1,
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        orden.refresh_from_db()
        self.assertEqual(orden.orden, 'ORD00099')

    def test_listado_muestra_campo_orden(self):
        from django.utils import timezone
        orden = Orden.objects.create(cliente=self.cliente, orden='ORDLISTA', estado_orden=self.estado_orden, created_at=timezone.now())
        url = reverse('ordenes_produccion_listar')
        response = self.client.get(url)
        self.assertContains(response, 'ORDLISTA')

    def test_bulk_crear_editar_eliminar_tres_ordenes(self):
        # Crear 3 órdenes
        codigos = ['ORDT01', 'ORDT02', 'ORDT03']
        for codigo in codigos:
            url = reverse('ordenes_produccion_nuevo') + '?fragment=1'
            data = {
                'cliente': self.cliente.id,
                'orden': codigo,
                'estado_orden': self.estado_orden.id,
                'prioridad': 1,
            }
            response = self.client.post(url, data, follow=True)
            self.assertEqual(response.status_code, 200)
            # Si hubiera errores de formulario, la plantilla incluiría este texto
            self.assertNotContains(response, 'Hay errores en el formulario')

        self.assertEqual(Orden.objects.count(), 3)

        # Editar cada una con un nuevo código
        for idx, orden in enumerate(Orden.objects.order_by('id')):
            nuevo_codigo = f"{codigos[idx]}E"
            url = reverse('ordenes_produccion_editar', args=[orden.id])
            data = {
                'cliente': self.cliente.id,
                'orden': nuevo_codigo,
                'estado_orden': self.estado_orden.id,
                'prioridad': 2,
            }
            # Usamos el header X-Fragment para evitar redirect y poder inspeccionar contenido
            response = self.client.post(url, data, follow=True, HTTP_X_FRAGMENT='1')
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, 'Hay errores en el formulario')
            orden.refresh_from_db()
            self.assertEqual(orden.orden, nuevo_codigo)

        # Eliminar las 3 órdenes
        ids = list(Orden.objects.values_list('id', flat=True))
        for oid in ids:
            url = reverse('ordenes_produccion_eliminar', args=[oid])
            response = self.client.post(url, follow=True)
            self.assertEqual(response.status_code, 200)

        self.assertEqual(Orden.objects.count(), 0)
from django.test import TestCase
from .models import Orden
from clientes.models import Cliente
from empleados.models import Empleado
from inventario_cafe.models import InventarioCafe
from estado_ordenes.models import EstadoOrden
from datetime import datetime

class OrdenCrudSQLServerTest(TestCase):
    reset_sequences = True

    def setUp(self):
        self.cliente = Cliente.objects.create(nombre="Test Cliente")
        self.empleado = Empleado.objects.create(nombres="Test", apellidos="Empleado", identificacion="9999")
        self.inven_cafe = InventarioCafe.objects.create()
        self.estado = EstadoOrden.objects.create(estado_orden="Pendiente")

    def test_crud_ordenes(self):
        # Crear 3 órdenes
        ordenes = []
        for i in range(3):
            orden = Orden.objects.create(
                cliente=self.cliente,
                id_empleado=self.empleado,
                id_inven_cafe=self.inven_cafe,
                estado_orden=self.estado,
                orden=f"ORD{i+1:02d}",
                fecha_inicio_orden=datetime.now(),
                prioridad=i+1,
                notas=f"Nota inicial {i+1}"
            )
            ordenes.append(orden)
        self.assertEqual(Orden.objects.count(), 3)

        # Editar cada orden
        for idx, orden in enumerate(ordenes):
            orden.prioridad = 10 + idx
            orden.notas = f"Editada {idx+1}"
            orden.orden = f"EDITSQL{idx+1}"
            orden.save()

        # Verificar edición
        for idx, orden in enumerate(Orden.objects.all()):
            self.assertEqual(orden.prioridad, 10 + idx)
            self.assertTrue(orden.notas.startswith("Editada"))
            self.assertTrue(orden.orden.startswith("EDITSQL"))

        # Eliminar cada orden
        for orden in ordenes:
            orden.delete()
        self.assertEqual(Orden.objects.count(), 0)


class OrdenModalStructureTests(TestCase):
    def setUp(self):
        from django.utils import timezone
        from empleados.models import Empleado
        from estado_ordenes.models import EstadoOrden
        from inventario_cafe.models import InventarioCafe

        self.cliente = Cliente.objects.create(nombre="Cliente ModalTest")
        self.empleado = Empleado.objects.create(nombres="John", apellidos="Doe", identificacion="MOD1")
        # Algunos campos pueden ser opcionales al renderizar GET del modal
        self.estado = EstadoOrden.objects.create(estado_orden="En Espera")
        self.inv = InventarioCafe.objects.create()

        self.orden = Orden.objects.create(
            cliente=self.cliente,
            id_empleado=self.empleado,
            id_inven_cafe=self.inv,
            estado_orden=self.estado,
            orden="ORDMOD1",
            fecha_inicio_orden=timezone.now(),
            prioridad=1,
        )

    def test_modal_footer_buttons_outside_body(self):
        from django.urls import reverse
        url = reverse('ordenes_produccion_editar', args=[self.orden.id])
        # Solicita el fragmento como lo hace el frontend (AJAX)
        resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)

        html = resp.content.decode('utf-8', errors='ignore')
        # Presencia de las secciones requeridas
        self.assertIn('data-modal-root', html)
        self.assertIn('modal-head', html)
        self.assertIn('modal-body', html)
        self.assertIn('modal-footer', html)

        body_start = html.find('class="modal-body')
        footer_start = html.find('class="modal-footer')
        self.assertNotEqual(body_start, -1, 'modal-body no encontrado')
        self.assertNotEqual(footer_start, -1, 'modal-footer no encontrado')
        self.assertGreater(footer_start, body_start, 'El footer debe ir después del body')

        body_section = html[body_start:footer_start]
        # No deben existir botones de acción dentro del body
        self.assertNotIn('data-close-modal', body_section)
        self.assertNotIn('type="submit"', body_section)
        self.assertNotIn('btn-primary', body_section)

        # Validar clases de comportamiento (crecen/encogen)
        self.assertIn('shrink-0', html)  # header/footer
        self.assertIn('grow overflow-y-auto', html)  # body scrolleable


class OrdenModalTemplateStaticTest(SimpleTestCase):
    def test_template_has_footer_after_body_and_no_buttons_in_body(self):
        import os
        from pathlib import Path
        # Lee el template directamente del disco para validación estática
        tpl_path = Path(__file__).resolve().parent / 'templates' / 'ordenes' / 'detail_OrdenesProduccion.html'
        self.assertTrue(tpl_path.exists(), f"No se encontró el template en {tpl_path}")
        html = tpl_path.read_text(encoding='utf-8')

        body_start = html.find('class="modal-body')
        footer_start = html.find('class="modal-footer')
        self.assertNotEqual(body_start, -1, 'modal-body no encontrado en template')
        self.assertNotEqual(footer_start, -1, 'modal-footer no encontrado en template')
        self.assertGreater(footer_start, body_start, 'El footer debe ir después del body en el template')

        body_section = html[body_start:footer_start]
        self.assertNotIn('data-close-modal', body_section)
        self.assertNotIn('type="submit"', body_section)
        self.assertNotIn('btn-primary', body_section)
