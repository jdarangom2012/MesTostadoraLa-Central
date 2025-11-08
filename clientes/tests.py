from django.test import TestCase
from django.urls import reverse
from .models import Cliente

class ClienteTests(TestCase):
    def setUp(self):
        # Crear datos mínimos para FK
        from tipo_clientes.models import TipoCliente
        from tipo_identificacion.models import TipoIdentificacion
        from estados_clientes.models import EstadoCliente
        self.tipo_cliente = TipoCliente.objects.create(tipo_cliente="Persona Natural")
        self.tipo_identificacion = TipoIdentificacion.objects.create(tipo_identificacion="CC")
        self.estado_cliente = EstadoCliente.objects.create(estado_cliente="Activo")

    def test_creacion_cliente_autogenera_codigo_cliente(self):
        url = reverse('cliente_nuevo')
        data = {
            'id_tipo_cliente': self.tipo_cliente.id,
            'id_tipo_identificacion': self.tipo_identificacion.id,
            'id_estado_cliente': self.estado_cliente.id,
            'codigo': '',
            'nombre': 'Juan',
            'apellidos': 'Pérez',
            'telefono': '123456789',
            'direccion': 'Calle 1',
            'email': 'juan@example.com',
            'representante_legal': '',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        cliente = Cliente.objects.latest('id')
        self.assertTrue(cliente.codigo_cliente)
        self.assertRegex(cliente.codigo_cliente, r'^CL-\d{6}$')

    def test_edicion_cliente_no_muestra_codigo_cliente_en_form(self):
        cliente = Cliente.objects.create(
            id_tipo_cliente=self.tipo_cliente,
            id_tipo_identificacion=self.tipo_identificacion,
            id_estado_cliente=self.estado_cliente,
            nombre='Ana',
            apellidos='Gómez',
            telefono='987654321',
            direccion='Calle 2',
            email='ana@example.com',
        )
        url = reverse('cliente_editar', args=[cliente.id])
        response = self.client.get(url)
        self.assertNotContains(response, 'name="codigo_cliente"')
        self.assertNotContains(response, 'Código Cliente')

    def test_listado_muestra_codigo_cliente(self):
        cliente = Cliente.objects.create(
            id_tipo_cliente=self.tipo_cliente,
            id_tipo_identificacion=self.tipo_identificacion,
            id_estado_cliente=self.estado_cliente,
            nombre='Luis',
            apellidos='Martínez',
            telefono='555555555',
            direccion='Calle 3',
            email='luis@example.com',
        )
        cliente.refresh_from_db(fields=["codigo_cliente"])
        url = reverse('clientes_listar')
        response = self.client.get(url)
        self.assertContains(response, cliente.codigo_cliente)

    def test_unicidad_codigo_cliente(self):
        # La BD debe rechazar duplicados
        cliente1 = Cliente.objects.create(
            id_tipo_cliente=self.tipo_cliente,
            id_tipo_identificacion=self.tipo_identificacion,
            id_estado_cliente=self.estado_cliente,
            nombre='Pedro',
            apellidos='Ramírez',
            telefono='111111111',
            direccion='Calle 4',
            email='pedro@example.com',
        )
        cliente1.refresh_from_db(fields=["codigo_cliente"])
        with self.assertRaises(Exception):
            Cliente.objects.create(
                id_tipo_cliente=self.tipo_cliente,
                id_tipo_identificacion=self.tipo_identificacion,
                id_estado_cliente=self.estado_cliente,
                nombre='Pedro2',
                apellidos='Ramírez2',
                telefono='222222222',
                direccion='Calle 5',
                email='pedro2@example.com',
                codigo_cliente=cliente1.codigo_cliente,
            )
