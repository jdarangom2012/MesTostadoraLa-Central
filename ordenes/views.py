from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db import IntegrityError, DatabaseError
from django import forms
from django.utils import timezone
from .models import Orden


class OrdenForm(forms.ModelForm):
    id_empleado = forms.ModelChoiceField(queryset=None, required=False)
    sacos_entero = forms.IntegerField(required=False, min_value=0)
    peso_bruto = forms.FloatField(required=False, min_value=0)
    peso = forms.FloatField(required=False, min_value=0)
    trabajo_empaque = forms.BooleanField(required=False)
    etiqueta_invima = forms.BooleanField(required=False)
    # Usar solo fecha (sin hora) en el formulario
    # Acepta DD/MM/YYYY y también ISO (fallback de los inputs type=date)
    fecha_inicio_orden = forms.DateField(required=False, input_formats=['%d/%m/%Y', '%Y-%m-%d'])
    fecha_entrega = forms.DateField(required=False, input_formats=['%d/%m/%Y', '%Y-%m-%d'])

    class Meta:
        model = Orden
        fields = [
            'orden',
            'cliente', 'estado_orden', 'estado_inven_cafe',
            'id_empleado',
            'fecha_inicio_orden', 'fecha_entrega', 'notas',
            'sacos_entero', 'peso_bruto', 'peso', 'trabajo_empaque', 'etiqueta_invima',
            'trilla', 'selec_cafe_verde', 'tueste_flag', 'selec_cafe_tostado',
            'molienda_flag', 'empaque_flag',
            'conf_trilla', 'conf_sel_verde', 'conf_tueste', 'conf_sel_tostado', 'conf_molienda', 'conf_empaque',
            'prioridad',
        ]
    widgets = {
        'id_empleado': forms.Select(attrs={'class': 'w-full select'}),
        'sacos_entero': forms.NumberInput(attrs={'class': 'w-full input', 'placeholder': 'Sacos enteros'}),
        'peso_bruto': forms.NumberInput(attrs={'class': 'w-full input', 'placeholder': 'Peso bruto (kg)', 'step': '0.01'}),
        'peso': forms.NumberInput(attrs={'class': 'w-full input', 'placeholder': 'Peso neto (kg)', 'step': '0.01'}),
        'trabajo_empaque': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        'etiqueta_invima': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        'orden': forms.TextInput(attrs={'class': 'w-full input', 'placeholder': 'Código de orden'}),
        'cliente': forms.Select(attrs={'class': 'w-full select'}),
        'estado_orden': forms.Select(attrs={'class': 'w-full select'}),
        'estado_inven_cafe': forms.Select(attrs={'class': 'w-full select'}),
        'fecha_inicio_orden': forms.TextInput(attrs={
            'data-datepicker': '1', 'class': 'w-full input', 'placeholder': 'DD/MM/YYYY', 'lang':'es-ES',
            'inputmode': 'numeric', 'autocomplete': 'off', 'pattern': '\d{2}/\d{2}/\d{4}'
        }),
        'fecha_entrega': forms.TextInput(attrs={
            'data-datepicker': '1', 'class': 'w-full input', 'placeholder': 'DD/MM/YYYY', 'lang':'es-ES',
            'inputmode': 'numeric', 'autocomplete': 'off', 'pattern': '\d{2}/\d{2}/\d{4}'
        }),
        'notas': forms.TextInput(attrs={'class': 'w-full input'}),
        'prioridad': forms.NumberInput(attrs={'class': 'w-full input'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from empleados.models import Empleado
        self.fields['id_empleado'].queryset = Empleado.objects.all()

    def clean_fecha_entrega(self):
        from django.utils import timezone
        from datetime import datetime
        d = self.cleaned_data.get('fecha_entrega')
        if d:
            dt = datetime.combine(d, datetime.min.time())
            return timezone.make_aware(dt)
        return d


@permission_required('ordenes.view_orden', raise_exception=True)
def listar_ordenes(request):
    qs = Orden.objects.select_related('cliente', 'estado_orden').order_by('-fecha_inicio_orden', '-id')
    search = request.GET.get('q', '').strip()
    if search:
        search_int = None
        try:
            search_int = int(search)
        except Exception:
            search_int = None
        q = (
            Q(cliente__nombre__icontains=search) |
            Q(cliente__apellidos__icontains=search)
            # ...otros filtros...
        )
        qs = qs.filter(q)
    paginator = Paginator(qs, 20)
    page = request.GET.get('page')
    try:
        ordenes = paginator.page(page)
    except PageNotAnInteger:
        ordenes = paginator.page(1)
    except EmptyPage:
        ordenes = paginator.page(paginator.num_pages)
    ctx = {
        'ordenes': ordenes,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'search': search
    }
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'ordenes/_modal_listar_OrdenesProduccion.html', ctx)
    return render(request, 'ordenes/listar_OrdenesProduccion.html', ctx)


@require_http_methods(["GET", "POST"])
@permission_required('ordenes.add_orden', raise_exception=True)
def add_orden(request):
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.fecha_ingreso:
                obj.fecha_ingreso = timezone.now()
            if not obj.created_at:
                obj.created_at = timezone.now()
            try:
                obj.save()
            except (IntegrityError, DatabaseError) as e:
                form.add_error(None, f'Error al guardar en base de datos: {e}')
            else:
                messages.success(request, 'Orden creada correctamente.')
                if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                    return listar_ordenes(request)
                return redirect('ordenes_produccion_listar')
    else:
        form = OrdenForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'ordenes/add_OrdenesProduccion.html', {'form': form})
    return render(request, 'ordenes/listar_OrdenesProduccion.html', {})


@require_http_methods(["GET", "POST"])
@permission_required('ordenes.change_orden', raise_exception=True)
def edit_orden(request, pk):
    obj = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        form = OrdenForm(request.POST, instance=obj)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.updated_at = timezone.now()
            try:
                inst.save()
            except (IntegrityError, DatabaseError) as e:
                form.add_error(None, f'Error al guardar en base de datos: {e}')
            else:
                messages.success(request, 'Orden actualizada correctamente.')
                if request.headers.get('X-Fragment'):
                    return listar_ordenes(request)
                return redirect('ordenes_produccion_listar')
    else:
        form = OrdenForm(instance=obj)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'ordenes/detail_OrdenesProduccion.html', {'form': form, 'obj': obj})
    return render(request, 'ordenes/listar_OrdenesProduccion.html', {})


@permission_required('ordenes.delete_orden', raise_exception=True)
def delete_orden(request, pk):
    obj = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        obj.delete()
        if request.headers.get('X-Fragment'):
            return listar_ordenes(request)
        return redirect('ordenes_produccion_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'ordenes/confirm_delete_OrdenesProduccion.html', {'obj': obj})
    return render(request, 'ordenes/listar_OrdenesProduccion.html', {})
