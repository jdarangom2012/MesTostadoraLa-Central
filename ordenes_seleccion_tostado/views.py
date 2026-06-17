from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from seguridad.decorators import permiso_accion_requerido
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms
from django.utils import timezone

from .models import OrdenSeleccionTostado
from ordenes.models import Orden
from estado_ordenes.models import EstadoOrden
from inventario_cafe.models import InventarioCafe
from clientes.models import Cliente


COMPLETADA_PESOS_ERROR = 'La tarea no se puede poner en estado completada porque uno o más pesos son menores o iguales a cero.'


class OrdenChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj)


class InventarioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Mostrar solo el código del inventario
        return obj.codigo or f"INV-{obj.id:06d}"


def obtener_estado_pendiente_seleccion_tostado():
    estado_pendiente = EstadoOrden.objects.filter(estado_orden__iexact='Pendiente').order_by('id').first()
    if estado_pendiente is not None:
        return estado_pendiente
    estado_pendiente, _ = EstadoOrden.objects.get_or_create(estado_orden='Pendiente')
    return estado_pendiente


class OrdenSeleccionTostadoForm(forms.ModelForm):
    orden = OrdenChoiceField(
        queryset=Orden.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full select'})
    )
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.none(),
        required=False,
        disabled=True,
        widget=forms.Select(attrs={'class': 'w-full select'})
    )
    inventario_cafe_ref = InventarioChoiceField(
        queryset=InventarioCafe.objects.all().order_by('-id'),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full select'})
    )
    estado_tareas = forms.ModelChoiceField(
        queryset=EstadoOrden.objects.all().order_by('estado_orden'),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full select'})
    )

    class Meta:
        model = OrdenSeleccionTostado
        fields = [
            'orden',
            'inventario_cafe_ref',
            'estado_tareas',
            'cat_limpieza',
            'cat_quaker','peso_quaker',
            'cat_grupo1','desc_grupo1','peso_grupo1',
            'cat_grupo2','desc_grupo2','peso_grupo2',
            'cat_grupo3','desc_grupo3','peso_grupo3',
            'notas',
        ]
        widgets = {
            'cat_limpieza': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'cat_quaker': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'peso_quaker': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'cat_grupo1': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'desc_grupo1': forms.TextInput(attrs={'class': 'w-full input'}),
            'peso_grupo1': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'cat_grupo2': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'desc_grupo2': forms.TextInput(attrs={'class': 'w-full input'}),
            'peso_grupo2': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'cat_grupo3': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'desc_grupo3': forms.TextInput(attrs={'class': 'w-full input'}),
            'peso_grupo3': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'notas': forms.Textarea(attrs={'class': 'w-full textarea', 'rows': '3', 'maxlength': '500'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_qs = Orden.objects.filter(selec_cafe_tostado=True).order_by('-id')
        estado_pendiente = obtener_estado_pendiente_seleccion_tostado()
        self.fields['cliente'].queryset = Cliente.objects.all().order_by('nombre', 'apellidos', 'id')
        if self.is_bound:
            self.fields['orden'].queryset = base_qs
        else:
            self.fields['orden'].queryset = base_qs.select_related('cliente')[:200]
        self.fields['orden'].empty_label = 'Seleccione una orden'
        self.fields['cliente'].empty_label = 'Seleccione un cliente'
        self.fields['inventario_cafe_ref'].empty_label = 'Seleccione un inventario café'
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
        if orden and not getattr(orden, 'selec_cafe_tostado', False):
            raise forms.ValidationError('Solo se permiten órdenes de producción con selección de tostado habilitada.')
        return orden

    def clean(self):
        cleaned_data = super().clean()
        estado_tareas = cleaned_data.get('estado_tareas')
        estado_nombre = (getattr(estado_tareas, 'estado_orden', '') or '').strip().lower()

        if estado_nombre != 'completada':
            return cleaned_data

        pesos_requeridos = (
            cleaned_data.get('peso_quaker'),
            cleaned_data.get('peso_grupo1'),
            cleaned_data.get('peso_grupo2'),
            cleaned_data.get('peso_grupo3'),
        )

        if any(peso is None or peso <= 0 for peso in pesos_requeridos):
            raise forms.ValidationError(COMPLETADA_PESOS_ERROR)

        return cleaned_data


def _build_orden_seleccion_tostado_defaults(orden):
    inventario_cafe = getattr(orden, 'id_inven_cafe', None)
    estado_pendiente = obtener_estado_pendiente_seleccion_tostado()
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
@permiso_accion_requerido('ordenes_seleccion_tostado.add_ordenselecciontostado', 'crear_orden_seleccion_tostado')
def orden_seleccion_tostado_defaults(request):
    orden_id = request.GET.get('orden_id')
    if not orden_id:
        return JsonResponse(_build_orden_seleccion_tostado_defaults(Orden()))

    try:
        orden = Orden.objects.select_related('id_inven_cafe', 'cliente').get(pk=orden_id, selec_cafe_tostado=True)
    except (TypeError, ValueError, Orden.DoesNotExist):
        return JsonResponse({'detail': 'Orden no encontrada.'}, status=404)

    return JsonResponse(_build_orden_seleccion_tostado_defaults(orden))


@permiso_accion_requerido('ordenes_seleccion_tostado.view_ordenselecciontostado', 'ver_orden_seleccion_tostado')
def listar_ordenes_seleccion_tostado(request):
    qs = (
        OrdenSeleccionTostado.objects
        .select_related('estado_tareas', 'orden', 'orden__cliente', 'cafe', 'inventario_cafe_ref')
        .order_by('-fecha_ingreso','-id')
    )
    search = request.GET.get('q', '').strip()
    if search:
        if search.isdigit():
            qs = qs.filter(id=int(search))
        else:
            qs = qs.filter(
                Q(estado_tareas__estado_orden__icontains=search) |
                Q(desc_grupo1__icontains=search) |
                Q(desc_grupo2__icontains=search) |
                Q(desc_grupo3__icontains=search)
            )

    paginator = Paginator(qs, 7)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    ctx = {
        'items': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'search': search,
    }
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'ordenes_seleccion_tostado/_modal_listar_OrdenesSelecionTostado.html', ctx)
    return render(request, 'ordenes_seleccion_tostado/listar_OrdenesSelecionTostado.html', ctx)


@require_http_methods(["GET","POST"])
@permiso_accion_requerido('ordenes_seleccion_tostado.add_ordenselecciontostado', 'crear_orden_seleccion_tostado')
def add_orden_seleccion_tostado(request):
    if request.method == 'POST':
        form = OrdenSeleccionTostadoForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.fecha_ingreso:
                obj.fecha_ingreso = timezone.now()
            obj.created_at = timezone.now()
            obj.updated_at = timezone.now()
            obj.save()
            if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                return listar_ordenes_seleccion_tostado(request)
            return redirect('ordenes_seleccion_tostado_listar')
    else:
        form = OrdenSeleccionTostadoForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'ordenes_seleccion_tostado/add_OrdenesSelecionTostado.html', {'form': form})
    return render(request, 'ordenes_seleccion_tostado/listar_OrdenesSelecionTostado.html', {})


@require_http_methods(["GET","POST"])
@permiso_accion_requerido('ordenes_seleccion_tostado.change_ordenselecciontostado', 'editar_orden_seleccion_tostado')
def edit_orden_seleccion_tostado(request, pk):
    obj = get_object_or_404(OrdenSeleccionTostado, pk=pk)
    if request.method == 'POST':
        form = OrdenSeleccionTostadoForm(request.POST, instance=obj)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.updated_at = timezone.now()
            inst.save()
            if request.headers.get('X-Fragment'):
                return listar_ordenes_seleccion_tostado(request)
            return redirect('ordenes_seleccion_tostado_listar')
    else:
        form = OrdenSeleccionTostadoForm(instance=obj)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'ordenes_seleccion_tostado/detail_OrdenesSelecionTostado.html', {'form': form, 'obj': obj})
    return render(request, 'ordenes_seleccion_tostado/listar_OrdenesSelecionTostado.html', {})


@permiso_accion_requerido('ordenes_seleccion_tostado.delete_ordenselecciontostado', 'eliminar_orden_seleccion_tostado')
def delete_orden_seleccion_tostado(request, pk):
    obj = get_object_or_404(OrdenSeleccionTostado, pk=pk)
    if request.method == 'POST':
        obj.delete()
        is_fragment = bool(request.headers.get('X-Fragment')) or request.POST.get('fragment') == '1'
        if is_fragment:
            return listar_ordenes_seleccion_tostado(request)
        return redirect('ordenes_seleccion_tostado_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'ordenes_seleccion_tostado/confirm_delete_OrdenesSelecionTostado.html', {'t': obj})
    return render(request, 'ordenes_seleccion_tostado/listar_OrdenesSelecionTostado.html', {})
