from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.db import transaction
from django.db.models import Max, Q
from django import forms
import re
from uuid import uuid4
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import DetalleTueste, Tueste
from ordenes.models import Orden
from seguridad.decorators import permiso_accion_requerido
from seguridad.helpers import puede_editar_campo, tiene_permiso_accion
from seguridad.models import PermisoCampo
from estado_ordenes.models import EstadoOrden
from estado_tareas.models import EstadoTarea
from nivel_tueste.models import NivelTueste
from inventario_cafe.models import InventarioCafe
from clientes.models import Cliente
def obtener_rol_usuario(user):
    perfil = getattr(user, 'perfilusuario', None) or getattr(user, 'profile', None)
    rol = getattr(perfil, 'rol', None)
    if rol is not None:
        return rol
    return None


def es_tostador(user) -> bool:
    rol = obtener_rol_usuario(user)
    nombre = getattr(rol, 'nombre', '')
    return str(nombre).strip().lower() == 'tostador'


def campos_editables_tostador(user):
    campos_base = {'peso_cafe_vede_total', 'peso_cafe_tostado_total'}
    rol = obtener_rol_usuario(user)
    if rol is None:
        return set()

    configurados = set(
        PermisoCampo.objects.filter(rol=rol, modelo='Tueste', campo__in=campos_base)
        .values_list('campo', flat=True)
        .distinct()
    )

    editables = set()
    for campo in campos_base:
        if campo not in configurados or puede_editar_campo(user, 'Tueste', campo):
            editables.add(campo)

    return editables


def aplicar_restricciones_form_tostador(form):
    user = getattr(form, '_request_user', None)
    campos_editables = campos_editables_tostador(user) if user is not None else set()

    for field_name, field in form.fields.items():
        if field_name in campos_editables:
            field.disabled = False
            field.widget.attrs.pop('disabled', None)
            field.widget.attrs.pop('readonly', None)
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{css} ring-1 ring-brand-primary/30".strip()
            continue

        if getattr(field.widget, 'input_type', '') in {'select', 'selectmultiple', 'checkbox', 'radio', 'file'}:
            field.disabled = True
            field.widget.attrs['disabled'] = 'disabled'
        else:
            field.widget.attrs['readonly'] = 'readonly'

        css = field.widget.attrs.get('class', '')
        field.widget.attrs['class'] = f"{css} bg-gray-100 text-gray-500 cursor-not-allowed".strip()
        field.widget.attrs['aria-readonly'] = 'true'


def proteger_campos_tostador(obj, original):
    campos_editables = campos_editables_tostador(getattr(obj, '_request_user', None))
    campos_protegidos = [
        'orden',
        'inventario_cafe_ref',
        'estado_tareas',
        'nivel_tueste',
        'batche',
        'peso_cafe_vede',
        'peso_cafe_tostado',
        'peso_cafe_vede_total',
        'peso_cafe_tostado_total',
        'notas',
        'notas_op',
    ]

    for campo in campos_protegidos:
        if campo in campos_editables:
            continue
        setattr(obj, campo, getattr(original, campo))


def calcular_rendimiento_tueste(peso_verde_total, peso_tostado_total):
    try:
        verde = float(peso_verde_total or 0)
    except (TypeError, ValueError):
        verde = 0.0

    try:
        tostado = float(peso_tostado_total or 0)
    except (TypeError, ValueError):
        tostado = 0.0

    if verde == 0:
        return 0.0

    return round((tostado / verde) * 100, 2)


def pesos_completan_tueste(peso_verde_total, peso_tostado_total):
    try:
        verde = float(peso_verde_total or 0)
    except (TypeError, ValueError):
        verde = 0.0

    try:
        tostado = float(peso_tostado_total or 0)
    except (TypeError, ValueError):
        tostado = 0.0

    return verde > 0 and tostado > 0


TUESTE_COMPLETADA_PESOS_ERROR = 'No es posible colocar el Tueste en estado Completada porque Peso Café Verde Total o Peso Café Tostado Total son menores o iguales a cero.'
TUESTE_COMPLETADA_TOSTADO_TOTAL_ERROR = 'No es posible colocar la Orden de Tueste en estado Completada porque el Peso Café Tostado Total es menor o igual a cero.'
TUESTE_COMPLETADA_BATCHES_ERROR = 'No es posible colocar el Tueste en estado Completada porque existen batches con Kilos Verdes o Kilos Tostado menores o iguales a cero.'


def estado_tarea_es_completada(estado_tareas):
    return (getattr(estado_tareas, 'estado_tareas', '') or '').strip().lower() == 'completada'


def batch_tiene_pesos_invalidos(batch):
    kilos_verde = getattr(batch, 'kilos_verde', None)
    kilos_tostado = getattr(batch, 'kilos_tostado', None)
    return kilos_verde is None or kilos_tostado is None or kilos_verde <= 0 or kilos_tostado <= 0


def hay_batches_validos_tostado(batches_qs):
    return any((getattr(batch, 'kilos_tostado', None) or 0) > 0 for batch in batches_qs)


def validar_tueste_completado(objeto_tueste, batches_qs=None):
    if not estado_tarea_es_completada(getattr(objeto_tueste, 'estado_tareas', None)):
        return

    objeto_tueste.sincronizar_peso_cafe_tostado_total()

    if (objeto_tueste.peso_cafe_tostado_total or 0) <= 0:
        raise forms.ValidationError(TUESTE_COMPLETADA_TOSTADO_TOTAL_ERROR)

    if not pesos_completan_tueste(objeto_tueste.peso_cafe_vede_total, objeto_tueste.peso_cafe_tostado_total):
        raise forms.ValidationError(TUESTE_COMPLETADA_PESOS_ERROR)

    batches_qs = list(batches_qs if batches_qs is not None else objeto_tueste.batches.all())
    if not hay_batches_validos_tostado(batches_qs):
        raise forms.ValidationError(TUESTE_COMPLETADA_TOSTADO_TOTAL_ERROR)

    if any(batch_tiene_pesos_invalidos(batch) for batch in batches_qs):
        raise forms.ValidationError(TUESTE_COMPLETADA_BATCHES_ERROR)


def tiene_campos_editables(user, objeto) -> bool:
    if getattr(user, 'is_superuser', False):
        return True

    if not objeto:
        return False

    modelo_perm = 'Tueste'
    campos_perm = [
        'orden',
        'inventario_cafe_ref',
        'estado_tareas',
        'nivel_tueste',
        'rendimiento',
        'peso_cafe_vede_total',
        'peso_cafe_tostado_total',
        'notas',
        'notas_op',
    ]

    configurados = set(
        PermisoCampo.objects.filter(modelo=modelo_perm, campo__in=campos_perm)
        .values_list('campo', flat=True)
        .distinct()
    )

    for campo in campos_perm:
        # Compatibilidad histórica: si el campo no tiene configuración explícita, se considera editable.
        if campo not in configurados:
            return True
        if puede_editar_campo(user, modelo_perm, campo):
            return True

    return False


class OrdenChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj)


class InventarioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.codigo or f"INV-{obj.id:06d}"


class TuesteForm(forms.ModelForm):
    orden = OrdenChoiceField(queryset=Orden.objects.none(), required=False, widget=forms.Select(attrs={'class':'w-full select'}))
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.none(), required=False, disabled=True, widget=forms.Select(attrs={'class':'w-full select'}))
    estado_tareas = forms.ModelChoiceField(queryset=EstadoTarea.objects.all().order_by('estado_tareas'), required=False, widget=forms.Select(attrs={'class':'w-full select'}))
    nivel_tueste = forms.ModelChoiceField(queryset=NivelTueste.objects.all().order_by('nivel_tueste'), required=False, widget=forms.Select(attrs={'class':'w-full select'}))
    inventario_cafe_ref = InventarioChoiceField(queryset=InventarioCafe.objects.all().order_by('-id'), required=False, widget=forms.Select(attrs={'class':'w-full select'}))

    class Meta:
        model = Tueste
        # fecha_ingreso es automática; no se expone en el formulario
        fields = ['orden','inventario_cafe_ref','estado_tareas','nivel_tueste','batche','peso_cafe_vede','peso_cafe_tostado','rendimiento','peso_cafe_vede_total','peso_cafe_tostado_total','notas','notas_op']
        widgets = {
            'batche': forms.NumberInput(attrs={'class':'w-full input', 'step':'1', 'min':'0'}),
            'peso_cafe_vede': forms.NumberInput(attrs={'class':'w-full input', 'step':'0.01'}),
            'peso_cafe_tostado': forms.NumberInput(attrs={'class':'w-full input', 'step':'0.01'}),
            'rendimiento': forms.NumberInput(attrs={'class':'w-full input', 'step':'0.01', 'readonly':'readonly'}),
            'peso_cafe_vede_total': forms.NumberInput(attrs={'class':'w-full input', 'step':'0.01'}),
            'peso_cafe_tostado_total': forms.NumberInput(attrs={'class':'w-full input', 'step':'0.01', 'readonly':'readonly'}),
            'notas': forms.TextInput(attrs={'class':'w-full input'}),
            'notas_op': forms.TextInput(attrs={'class':'w-full input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_qs = Orden.objects.filter(tueste_flag=True).order_by('-id')
        estado_pendiente = EstadoTarea.objects.filter(estado_tareas__iexact='Pendiente').order_by('id').first()
        self.fields['cliente'].queryset = Cliente.objects.all().order_by('nombre', 'apellidos', 'id')
        if self.is_bound:
            self.fields['orden'].queryset = base_qs
        else:
            self.fields['orden'].queryset = base_qs.select_related('cliente')[:200]
        self.fields['orden'].empty_label = 'Seleccione una orden'
        self.fields['cliente'].empty_label = 'Seleccione un cliente'
        self.fields['inventario_cafe_ref'].empty_label = 'Seleccione un café'
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

    def clean_orden(self):
        orden = self.cleaned_data.get('orden')
        if orden and not getattr(orden, 'tueste_flag', False):
            raise forms.ValidationError('Solo se permiten órdenes de producción con tueste habilitado.')
        return orden

    def clean(self):
        return super().clean()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.batche = 0
        instance.peso_cafe_vede = 0
        instance.peso_cafe_tostado = 0
        instance.sincronizar_peso_cafe_tostado_total()

        if commit:
            instance.save()

        return instance


class DetalleTuesteForm(forms.ModelForm):
    nivel_tueste = forms.ModelChoiceField(
        queryset=NivelTueste.objects.all().order_by('nivel_tueste'),
        required=False,
        widget=forms.Select(attrs={'class':'w-full select'})
    )
    estado_orden = forms.ModelChoiceField(
        queryset=EstadoOrden.objects.all().order_by('estado_orden', 'id'),
        required=False,
        widget=forms.Select(attrs={'class':'w-full select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound or getattr(self.instance, 'pk', None):
            return

        estado_pendiente = EstadoOrden.objects.filter(estado_orden__iexact='Pendiente').order_by('id').first()
        if estado_pendiente is not None:
            self.initial.setdefault('estado_orden', estado_pendiente.pk)

    class Meta:
        model = DetalleTueste
        fields = ['estado_orden', 'nivel_tueste', 'kilos_verde', 'kilos_tostado', 'observaciones']
        widgets = {
            'kilos_verde': forms.NumberInput(attrs={'class':'w-full input', 'step':'0.01', 'min':'0'}),
            'kilos_tostado': forms.NumberInput(attrs={'class':'w-full input', 'step':'0.01', 'min':'0'}),
            'observaciones': forms.TextInput(attrs={'class':'w-full input', 'maxlength':'500'}),
        }

    def clean_kilos_verde(self):
        kilos_verde = self.cleaned_data.get('kilos_verde')
        if kilos_verde is not None and kilos_verde < 0:
            raise forms.ValidationError('Los kilos verdes deben ser mayores o iguales a 0.')
        return kilos_verde

    def clean_kilos_tostado(self):
        kilos_tostado = self.cleaned_data.get('kilos_tostado')
        if kilos_tostado is not None and kilos_tostado < 0:
            raise forms.ValidationError('Los kilos tostado deben ser mayores o iguales a 0.')
        return kilos_tostado

    def clean(self):
        cleaned_data = super().clean()
        self.instance.estado_orden = cleaned_data.get('estado_orden')
        self.instance.kilos_verde = cleaned_data.get('kilos_verde')
        self.instance.kilos_tostado = cleaned_data.get('kilos_tostado')

        try:
            self.instance.validar_estado_orden_con_pesos()
        except ValidationError as exc:
            self.add_error(None, exc.message)

        return cleaned_data


def obtener_batches_tueste(tueste):
    return tueste.batches.select_related('nivel_tueste', 'estado_orden').all()


def validar_batch_estado_orden(form, detalle):
    detalle.estado_orden = form.cleaned_data.get('estado_orden')
    detalle.kilos_verde = form.cleaned_data.get('kilos_verde')
    detalle.kilos_tostado = form.cleaned_data.get('kilos_tostado')
    detalle.validar_estado_orden_con_pesos()


def _build_orden_tueste_defaults(orden):
    inventario_cafe = getattr(orden, 'id_inven_cafe', None)
    estado_pendiente = EstadoTarea.objects.filter(estado_tareas__iexact='Pendiente').order_by('id').first()
    cliente = getattr(orden, 'cliente', None)

    return {
        'cliente_id': getattr(cliente, 'id', None),
        'cliente_label': str(cliente) if cliente is not None else '',
        'inventario_cafe_ref_id': getattr(inventario_cafe, 'id', None),
        'inventario_cafe_ref_label': str(inventario_cafe) if inventario_cafe is not None else '',
        'estado_tareas_id': getattr(estado_pendiente, 'id', None),
        'estado_tareas_label': str(estado_pendiente) if estado_pendiente is not None else '',
    }


@require_http_methods(["GET"])
@permiso_accion_requerido('tueste.add_tueste', 'crear_orden_tueste')
def orden_tueste_defaults(request):
    orden_id = request.GET.get('orden_id')
    if not orden_id:
        return JsonResponse(_build_orden_tueste_defaults(Orden()))

    try:
        orden = Orden.objects.select_related('id_inven_cafe', 'cliente').get(pk=orden_id, tueste_flag=True)
    except (TypeError, ValueError, Orden.DoesNotExist):
        return JsonResponse({'detail': 'Orden no encontrada.'}, status=404)

    return JsonResponse(_build_orden_tueste_defaults(orden))


def siguiente_numero_batch(tueste):
    ultimo = tueste.batches.aggregate(max_batch=Max('numero_batch')).get('max_batch') or 0
    return ultimo + 1


def construir_contexto_tueste(request, tueste, form=None):
    form = form or TuesteForm(instance=tueste)
    form._request_user = request.user
    user_is_tostador = es_tostador(request.user)
    if user_is_tostador:
        aplicar_restricciones_form_tostador(form)

    return {
        'form': form,
        'tueste': tueste,
        'detalle_batches': obtener_batches_tueste(tueste),
        'user_is_tostador': user_is_tostador,
    }


def render_editar_tueste(request, tueste, form=None):
    return render(request, 'tueste/detail_OrdenesTueste.html', construir_contexto_tueste(request, tueste, form=form))


@permiso_accion_requerido('tueste.view_tueste', 'ver_orden_tueste')
def listar_ordenes_tueste(request):
    qs = Tueste.objects.select_related('orden__cliente','estado_tareas','nivel_tueste','inventario_cafe_ref')
    search = request.GET.get('q','').strip()
    if search:
        s = search.strip()
        filters = (
            Q(orden__cliente__nombre__icontains=s) |
            Q(orden__cliente__apellidos__icontains=s)
        )
        m = re.search(r"(?:^|\b)orden\s*(\d+)\b", s, flags=re.IGNORECASE)
        if m:
            try:
                filters |= Q(orden__id=int(m.group(1)))
            except ValueError:
                pass
        else:
            m2 = re.search(r"\b(\d+)\b", s)
            if m2:
                try:
                    filters |= Q(orden__id=int(m2.group(1)))
                except ValueError:
                    pass
        qs = qs.filter(filters)

    qs = qs.order_by('-fecha_ingreso','-id')

    paginator = Paginator(qs, 7)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    puede_editar_tueste = tiene_permiso_accion(request.user, django_perm='tueste.change_tueste', codigo='editar_orden_tueste')
    puede_eliminar_tueste = tiene_permiso_accion(request.user, django_perm='tueste.delete_tueste', codigo='eliminar_orden_tueste')

    for tueste in page_obj.object_list:
        tueste.puede_editar = puede_editar_tueste and tiene_campos_editables(request.user, tueste)
        tueste.puede_eliminar = puede_eliminar_tueste

    ctx = {
        'tuestes': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'search': search,
        'puede_editar_tueste': puede_editar_tueste,
        'puede_eliminar_tueste': puede_eliminar_tueste,
    }
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'tueste/_modal_listar_OrdenesTueste.html', ctx)
    return render(request, 'tueste/listar_OrdenesTueste.html', ctx)


@require_http_methods(["GET","POST"])
@permiso_accion_requerido('tueste.add_tueste', 'crear_orden_tueste')
def add_orden_tueste(request):
    is_fragment = request.GET.get('fragment') == '1' or request.headers.get('X-Fragment')

    def new_submit_token():
        return uuid4().hex

    def render_form(form):
        return render(request, 'tueste/add_OrdenesTueste.html', {
            'form': form,
            'submit_token': new_submit_token(),
            'detalle_batches': [],
        })

    def duplicate_response():
        if is_fragment:
            return listar_ordenes_tueste(request)
        return redirect('ordenes_tueste_listar')

    if request.method == 'POST':
        form = TuesteForm(request.POST)
        if form.is_valid():
            submitted_flag = request.POST.get('_submitted')
            submission_token = request.POST.get('_submission_token', '').strip()

            if submitted_flag == '1':
                token_key = f"tueste:add:submit:{submission_token}"
                if not submission_token or not cache.add(token_key, True, timeout=300):
                    return duplicate_response()

            obj = form.save(commit=False)
            obj.rendimiento = calcular_rendimiento_tueste(
                obj.peso_cafe_vede_total,
                obj.peso_cafe_tostado_total,
            )
            obj.fecha_ingreso = timezone.now()
            obj.created_at = timezone.now()
            obj.updated_at = timezone.now()
            try:
                validar_tueste_completado(obj, batches_qs=[])
            except forms.ValidationError as exc:
                form.add_error(None, exc.message)
            else:
                obj.save()
                if is_fragment:
                    return listar_ordenes_tueste(request)
                return redirect('ordenes_tueste_listar')
    else:
        form = TuesteForm()
    if is_fragment:
        return render_form(form)
    return render(request, 'tueste/listar_OrdenesTueste.html', {})


@require_http_methods(["GET","POST"])
@permiso_accion_requerido('tueste.change_tueste', 'editar_orden_tueste')
def edit_orden_tueste(request, pk):
    tueste = get_object_or_404(Tueste, pk=pk)
    user_is_tostador = es_tostador(request.user)

    if request.method == 'POST':
        form = TuesteForm(request.POST, instance=tueste)
        form._request_user = request.user
        if form.is_valid():
            obj = form.save(commit=False)
            obj._request_user = request.user
            if user_is_tostador:
                proteger_campos_tostador(obj, tueste)
            obj.rendimiento = calcular_rendimiento_tueste(
                obj.peso_cafe_vede_total,
                obj.peso_cafe_tostado_total,
            )
            obj.updated_at = timezone.now()
            try:
                validar_tueste_completado(obj, batches_qs=tueste.batches.all())
            except forms.ValidationError as exc:
                form.add_error(None, exc.message)
            else:
                obj.save()
                if request.headers.get('X-Fragment'):
                    return listar_ordenes_tueste(request)
                return redirect('ordenes_tueste_listar')
    else:
        form = TuesteForm(instance=tueste)
        form._request_user = request.user

    if user_is_tostador:
        aplicar_restricciones_form_tostador(form)

    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render_editar_tueste(request, tueste, form=form)
    return render(request, 'tueste/listar_OrdenesTueste.html', {})


@permiso_accion_requerido('tueste.delete_tueste', 'eliminar_orden_tueste')
def delete_orden_tueste(request, pk):
    t = get_object_or_404(Tueste, pk=pk)
    if request.method == 'POST':
        t.delete()
        if request.headers.get('X-Fragment'):
            return listar_ordenes_tueste(request)
        return redirect('ordenes_tueste_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'tueste/confirm_delete_OrdenesTueste.html', {'t': t})
    return render(request, 'tueste/listar_OrdenesTueste.html', {})


@require_http_methods(["GET", "POST"])
@permiso_accion_requerido('tueste.change_tueste', 'editar_orden_tueste')
def add_batch_tueste(request, pk):
    tueste = get_object_or_404(Tueste, pk=pk)
    numero_batch = siguiente_numero_batch(tueste)

    if request.method == 'POST':
        form = DetalleTuesteForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.tueste = tueste
            detalle.numero_batch = siguiente_numero_batch(tueste)
            detalle.fecha_ingreso = timezone.now()

            try:
                validar_batch_estado_orden(form, detalle)
            except ValidationError as exc:
                form.add_error(None, exc.message)
            else:
                with transaction.atomic():
                    detalle.save()
                    tueste.sincronizar_peso_cafe_tostado_total()
                    tueste.updated_at = timezone.now()
                    tueste.save(update_fields=['peso_cafe_tostado_total', 'updated_at'])
                if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                    return render_editar_tueste(request, tueste)
                return redirect('orden_tueste_editar', pk=tueste.pk)
    else:
        form = DetalleTuesteForm()

    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'tueste/batch_OrdenesTueste.html', {
            'form': form,
            'tueste': tueste,
            'detalle': None,
            'numero_batch': numero_batch,
        })
    return redirect('orden_tueste_editar', pk=tueste.pk)


@require_http_methods(["GET", "POST"])
@permiso_accion_requerido('tueste.change_tueste', 'editar_orden_tueste')
def edit_batch_tueste(request, pk, detalle_pk):
    tueste = get_object_or_404(Tueste, pk=pk)
    detalle = get_object_or_404(DetalleTueste, pk=detalle_pk, tueste=tueste)

    if request.method == 'POST':
        form = DetalleTuesteForm(request.POST, instance=detalle)
        if form.is_valid():
            detalle_actualizado = form.save(commit=False)
            if not detalle_actualizado.fecha_ingreso:
                detalle_actualizado.fecha_ingreso = timezone.now()

            try:
                validar_batch_estado_orden(form, detalle_actualizado)
            except ValidationError as exc:
                form.add_error(None, exc.message)
            else:
                detalle_actualizado.save()
                tueste.sincronizar_peso_cafe_tostado_total()
                tueste.updated_at = timezone.now()
                tueste.save(update_fields=['peso_cafe_tostado_total', 'updated_at'])
                if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                    return render_editar_tueste(request, tueste)
                return redirect('orden_tueste_editar', pk=tueste.pk)
    else:
        form = DetalleTuesteForm(instance=detalle)

    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'tueste/batch_OrdenesTueste.html', {
            'form': form,
            'tueste': tueste,
            'detalle': detalle,
            'numero_batch': detalle.numero_batch,
        })
    return redirect('orden_tueste_editar', pk=tueste.pk)
