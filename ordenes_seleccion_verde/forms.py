from django import forms

from clientes.models import Cliente
from estado_tareas.models import EstadoTarea
from ordenes.models import Orden
from seguridad.helpers import puede_editar_campo, puede_ver_campo
from zaranda_grupo.models import ZarandaGrupo

from .models import OrdenSeleccionVerde


COMPLETADA_PESOS_ERROR = 'La tarea no se puede poner en estado completada porque uno o más pesos son menores o iguales a cero.'


class OrdenSeleccionVerdeForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.none(),
        required=False,
        disabled=True,
        widget=forms.Select(attrs={'class': 'w-full select'})
    )
    estado_tareas = forms.ModelChoiceField(
        queryset=EstadoTarea.objects.all().order_by('estado_tareas'),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full select'})
    )

    class Meta:
        model = OrdenSeleccionVerde
        fields = [
            'orden',
            'estado_tareas',
            'zaranda',
            'IdZarandaGrupo1', 'peso_grupo1',
            'IdZarandaGrupo2', 'peso_grupo2',
            'IdZarandaGrupo3', 'peso_grupo3',
            'IdZarandaGrupo4', 'peso_grupo4',
            'IdZarandaGrupo5', 'peso_grupo5',
            'peso_grupo_ripio',
            'catadora',
            'catacion_ripio', 'peso_cat_ripio',
            'catacion_balsos', 'peso_cat_balsos',
            'catacion_grupo1', 'peso_cat_grupo1',
            'catacion_grupo2', 'peso_cat_grupo2',
            'peso_aceptado',
            'medir_humedad', 'humedad',
            'medir_densidad', 'densidad',
            'notas',
        ]
        widgets = {
            'orden': forms.Select(attrs={'class': 'w-full select'}),
            'zaranda': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'IdZarandaGrupo1': forms.Select(attrs={'class': 'w-full select'}),
            'peso_grupo1': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'IdZarandaGrupo2': forms.Select(attrs={'class': 'w-full select'}),
            'peso_grupo2': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'IdZarandaGrupo3': forms.Select(attrs={'class': 'w-full select'}),
            'peso_grupo3': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'IdZarandaGrupo4': forms.Select(attrs={'class': 'w-full select'}),
            'peso_grupo4': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'IdZarandaGrupo5': forms.Select(attrs={'class': 'w-full select'}),
            'peso_grupo5': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'peso_grupo_ripio': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'catadora': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'catacion_ripio': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'peso_cat_ripio': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'catacion_balsos': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'peso_cat_balsos': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'catacion_grupo1': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'peso_cat_grupo1': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'catacion_grupo2': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'peso_cat_grupo2': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'peso_aceptado': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'medir_humedad': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'humedad': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01', 'min': '0', 'max': '100'}),
            'medir_densidad': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'densidad': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'notas': forms.Textarea(attrs={'class': 'w-full input', 'rows': '3', 'maxlength': '500'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        estado_pendiente = EstadoTarea.objects.filter(estado_tareas__iexact='Pendiente').order_by('id').first()

        if 'zaranda' in self.fields:
            self.fields['zaranda'].widget.attrs['onchange'] = "window.initSeleccionVerdeZaranda && window.initSeleccionVerdeZaranda(this.closest('[data-modal-root]') || document)"

        if 'orden' in self.fields:
            base_qs = Orden.objects.filter(selec_cafe_verde=True).order_by('-id')
            self.fields['cliente'].queryset = Cliente.objects.all().order_by('nombre', 'apellidos', 'id')
            if self.is_bound:
                self.fields['orden'].queryset = base_qs
            else:
                self.fields['orden'].queryset = base_qs.select_related('cliente')[:200]
            self.fields['orden'].required = False
            self.fields['orden'].empty_label = 'Seleccione una orden'
            self.fields['cliente'].empty_label = 'Seleccione un cliente'
            cliente = None
            orden_id = self.data.get('orden') if self.is_bound else None
            if orden_id:
                try:
                    cliente = base_qs.select_related('cliente').get(pk=orden_id).cliente
                except (TypeError, ValueError, Orden.DoesNotExist):
                    cliente = None
            elif getattr(self.instance, 'orden', None) is not None:
                cliente = getattr(self.instance.orden, 'cliente', None)
            if cliente is not None:
                self.fields['cliente'].initial = cliente.pk
                self.initial['cliente'] = cliente.pk

        if estado_pendiente is not None and not getattr(self.instance, 'pk', None) and not self.is_bound:
            self.fields['estado_tareas'].initial = estado_pendiente.pk
            self.initial['estado_tareas'] = estado_pendiente.pk

        zaranda_enabled = False
        if self.is_bound:
            raw_value = self.data.get('zaranda')
            zaranda_enabled = raw_value in ('on', 'true', 'True', '1')
        elif getattr(self.instance, 'pk', None):
            zaranda_enabled = bool(getattr(self.instance, 'zaranda', False))
        else:
            zaranda_enabled = bool(self.initial.get('zaranda', False))

        target_fields = (
            'IdZarandaGrupo1',
            'IdZarandaGrupo2',
            'IdZarandaGrupo3',
            'IdZarandaGrupo4',
            'IdZarandaGrupo5',
            'peso_grupo1',
            'peso_grupo2',
            'peso_grupo3',
            'peso_grupo4',
            'peso_grupo5',
        )

        for field_name in target_fields:
            if field_name not in self.fields:
                continue
            widget = self.fields[field_name].widget
            existing_class = widget.attrs.get('class', '')
            if not zaranda_enabled:
                widget.attrs['readonly'] = 'readonly'
                if field_name.startswith('IdZarandaGrupo'):
                    widget.attrs['aria-readonly'] = 'true'
                    widget.attrs['tabindex'] = '-1'
                    widget.attrs['style'] = 'pointer-events: none;'
                widget.attrs['class'] = (existing_class + ' bg-gray-200 cursor-not-allowed').strip()
            else:
                widget.attrs.pop('readonly', None)
                widget.attrs.pop('aria-readonly', None)
                widget.attrs.pop('tabindex', None)
                if widget.attrs.get('style') == 'pointer-events: none;':
                    widget.attrs.pop('style', None)
                cleaned = existing_class.replace('bg-gray-200', '').replace('cursor-not-allowed', '')
                widget.attrs['class'] = ' '.join(cleaned.split())

        zg_qs = ZarandaGrupo.objects.all().order_by('zaranda_grupo', 'id')
        for field_name in (
            'IdZarandaGrupo1',
            'IdZarandaGrupo2',
            'IdZarandaGrupo3',
            'IdZarandaGrupo4',
            'IdZarandaGrupo5',
        ):
            if field_name not in self.fields:
                continue
            field = self.fields[field_name]
            field.queryset = zg_qs
            field.required = False

        self._permisos_campo = {}
        user = self.user
        if not user or not getattr(user, 'is_authenticated', False):
            return

        # Admin sin restricciones
        if getattr(user, 'is_superuser', False):
            return

        # Mantener compatibilidad: soportar user.profile (proyecto) y user.perfilusuario (si existiera)
        perfil = getattr(user, 'perfilusuario', None) or getattr(user, 'profile', None)
        rol = getattr(perfil, 'rol', None)
        if not rol:
            return

        # Permisos por campo
        from seguridad.models import PermisoCampo

        permisos = PermisoCampo.objects.filter(rol=rol, modelo='OrdenSeleccionVerde')
        permisos_dict = {p.campo: p for p in permisos}
        self._permisos_campo = permisos_dict

        for field_name, field in self.fields.items():
            permiso = permisos_dict.get(field_name)
            if not permiso:
                continue

            # Si NO puede ver → ocultar
            if not permiso.puede_ver:
                field.widget = forms.HiddenInput()
                field.required = False
                continue

            # Si NO puede editar → deshabilitar (readonly no bloquea selects/checkboxes)
            if not permiso.puede_editar:
                field.disabled = True
                field.widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()

        # Validación defensiva: aunque manipulen el POST, no permitir cambios en campos
        # ocultos o sin permiso de edición.
        def _enforce_field_permissions():
            user = getattr(self, 'user', None)
            if user and getattr(user, 'is_superuser', False):
                return

            permisos_dict = getattr(self, '_permisos_campo', None) or {}
            if not permisos_dict:
                return

            for field_name, permiso in permisos_dict.items():
                if getattr(permiso, 'puede_ver', True) and getattr(permiso, 'puede_editar', True):
                    continue
                if field_name not in cleaned_data:
                    continue

                if getattr(self.instance, 'pk', None) and hasattr(self.instance, field_name):
                    cleaned_data[field_name] = getattr(self.instance, field_name)
                else:
                    cleaned_data.pop(field_name, None)

        # 1) Antes de validaciones/ajustes: para que usen valores permitidos
        _enforce_field_permissions()

        orden = cleaned_data.get('orden')
        if orden and not getattr(orden, 'selec_cafe_verde', False):
            self.add_error('orden', 'Solo se permiten órdenes de producción con selección verde habilitada.')

        grupos = [
            ('IdZarandaGrupo1', 'peso_grupo1'),
            ('IdZarandaGrupo2', 'peso_grupo2'),
            ('IdZarandaGrupo3', 'peso_grupo3'),
            ('IdZarandaGrupo4', 'peso_grupo4'),
            ('IdZarandaGrupo5', 'peso_grupo5'),
        ]

        todo_valido = True

        for campo_grupo, campo_peso in grupos:
            grupo = cleaned_data.get(campo_grupo)
            peso = cleaned_data.get(campo_peso) or 0

            if not grupo:
                continue

            nombre_grupo = str(grupo or '').strip()
            if nombre_grupo.upper() != 'N/A' and peso <= 0:
                todo_valido = False
                self.add_error(
                    campo_peso,
                    'Debe ser mayor a 0 cuando la malla seleccionada no es N/A.'
                )

        estado_tareas = cleaned_data.get('estado_tareas')
        estado_nombre = (getattr(estado_tareas, 'estado_tareas', '') or '').strip().lower()
        if estado_nombre == 'completada':
            pesos_requeridos = (
                cleaned_data.get('peso_grupo1'),
                cleaned_data.get('peso_grupo2'),
                cleaned_data.get('peso_grupo3'),
                cleaned_data.get('peso_grupo4'),
                cleaned_data.get('peso_grupo5'),
                cleaned_data.get('peso_grupo_ripio'),
                cleaned_data.get('peso_cat_ripio'),
                cleaned_data.get('peso_cat_balsos'),
                cleaned_data.get('peso_cat_grupo1'),
                cleaned_data.get('peso_cat_grupo2'),
                cleaned_data.get('peso_aceptado'),
            )
            if any(peso is None or peso <= 0 for peso in pesos_requeridos):
                raise forms.ValidationError(COMPLETADA_PESOS_ERROR)

        # 2) Al final: por si el clean() modificó algo no editable
        _enforce_field_permissions()

        return cleaned_data

    def clean_orden(self):
        orden = self.cleaned_data.get('orden')
        if orden and not getattr(orden, 'selec_cafe_verde', False):
            raise forms.ValidationError('Solo se permiten órdenes de producción con selección verde habilitada.')
        return orden
