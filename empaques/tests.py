from django.test import TestCase

from cafe_empaque.models import CafeEmpaque
from clientes.models import Cliente
from estado_tareas.models import EstadoTarea
from nivel_molienda.models import NivelMolienda
from ordenes.models import Orden
from tamano_empaque.models import TamanoEmpaque

from empaques.forms import EmpaqueForm, build_detalle_empaque_formset
from empaques.models import Empaque
from empaques.views import sincronizar_resumen_empaque


class EmpaqueDetalleFormsetTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nombre='Cliente', apellidos='Empaque')
        self.orden = Orden.objects.create(orden='OP-EMP-001', cliente=self.cliente)
        self.estado = EstadoTarea.objects.create(estado_tareas='Pendiente')
        self.empaque_cafe = CafeEmpaque.objects.create(empaque_cafe='Bolsa valvula')
        self.tamano = TamanoEmpaque.objects.create(tamano_empaque='500g')
        self.molienda = NivelMolienda.objects.create(nivel_molienda='Media')

    def _detalle_management(self, total_forms, initial_forms=0):
        return {
            'detalle_empaque-TOTAL_FORMS': str(total_forms),
            'detalle_empaque-INITIAL_FORMS': str(initial_forms),
            'detalle_empaque-MIN_NUM_FORMS': '0',
            'detalle_empaque-MAX_NUM_FORMS': '1000',
        }

    def test_nuevo_empaque_requiere_al_menos_una_linea(self):
        form = EmpaqueForm(
            data={
                'orden': self.orden.pk,
                'estado_tareas': self.estado.pk,
                'cant_etiquetas': '10',
                'emp_clientes': '5',
                'notas': 'Prueba',
            }
        )
        formset = build_detalle_empaque_formset(
            data={
                **self._detalle_management(total_forms=1),
                'detalle_empaque-0-empaque_cafe': '',
                'detalle_empaque-0-tamano_empaque': '',
                'detalle_empaque-0-pedido': '',
                'detalle_empaque-0-empacado': '',
                'detalle_empaque-0-nivel_molienda': '',
                'detalle_empaque-0-notas': '',
            },
            instance=form.instance,
        )

        self.assertTrue(form.is_valid())
        self.assertFalse(formset.is_valid())
        self.assertIn('Debe registrar al menos una linea de empaque.', formset.non_form_errors()[0])

    def test_cliente_se_inicializa_desde_la_orden_en_formulario_enlazado(self):
        form = EmpaqueForm(
            data={
                'orden': str(self.orden.pk),
                'estado_tareas': str(self.estado.pk),
                'cant_etiquetas': '3',
                'emp_clientes': '2',
                'notas': 'Con cliente',
            }
        )

        self.assertEqual(form.initial.get('cliente'), self.cliente.pk)
        self.assertEqual(form.fields['cliente'].initial, self.cliente.pk)
        self.assertIn('data-cliente-id="%s"' % self.cliente.pk, str(form['orden']))

    def test_sincroniza_totales_y_referencias_desde_el_detalle(self):
        empaque = Empaque.objects.create(orden=self.orden, estado_tareas=self.estado, notas='Base')
        formset = build_detalle_empaque_formset(
            data={
                **self._detalle_management(total_forms=1),
                'detalle_empaque-0-id': '',
                'detalle_empaque-0-empaque_cafe': str(self.empaque_cafe.pk),
                'detalle_empaque-0-tamano_empaque': str(self.tamano.pk),
                'detalle_empaque-0-pedido': '25',
                'detalle_empaque-0-empacado': '20',
                'detalle_empaque-0-nivel_molienda': str(self.molienda.pk),
                'detalle_empaque-0-notas': 'Fila 1',
                'detalle_empaque-0-suministro': 'on',
            },
            instance=empaque,
        )

        self.assertTrue(formset.is_valid(), formset.errors)
        formset.save()
        sincronizar_resumen_empaque(empaque)
        empaque.refresh_from_db()

        self.assertEqual(empaque.cant_empaque, 25)
        self.assertEqual(empaque.cant_empacada, 20)
        self.assertEqual(empaque.total_empaques, 25)
        self.assertEqual(empaque.total_paquetes, 20)
        self.assertEqual(empaque.tamano_id, self.tamano.pk)
        self.assertEqual(empaque.nivel_molienda_id, self.molienda.pk)
        self.assertEqual(empaque.detalles.count(), 1)