from django.test import TestCase
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
        perms = Permission.objects.filter(codename__in=['add_orden', 'change_orden', 'view_orden'])
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
