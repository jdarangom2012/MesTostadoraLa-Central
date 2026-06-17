from django.shortcuts import render, get_object_or_404, redirect
from seguridad.decorators import permiso_accion_requerido
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.db import DatabaseError, IntegrityError
from django.db.models import Q
from django import forms
from django.utils import timezone
from django.urls import reverse
from urllib.parse import urlencode

from .models import InventarioCafe
from origen_cafe.models import OrigenCafe
from proceso_inven_cafe.models import ProcesoInvenCafe
from variedad_cafe.models import VariedadCafe
from clientes.models import Cliente
from estado_cafe.models import EstadoCafe
from cafe_empaque.models import CafeEmpaque


class CodigoSourceSelect(forms.Select):
    def __init__(self, *args, codigo_attr=None, **kwargs):
        self.codigo_attr = codigo_attr
        super().__init__(*args, **kwargs)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        instance = getattr(value, 'instance', None)
        if instance is not None and self.codigo_attr:
            option['attrs']['data-codigo-value'] = getattr(instance, self.codigo_attr, '') or ''
        return option


class InventarioCafeForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all().order_by('nombre'), required=False, widget=CodigoSourceSelect(codigo_attr='nombre', attrs={'class': 'w-full select', 'data-codigo-source': 'cliente', 'data-codigo-length': '6'}))
    estado_cafe = forms.ModelChoiceField(queryset=EstadoCafe.objects.all().order_by('estado_cafe'), required=False, widget=CodigoSourceSelect(codigo_attr='estado_cafe', attrs={'class': 'w-full select', 'data-codigo-source': 'estado', 'data-codigo-length': '3'}))
    empaquecafe = forms.ModelChoiceField(queryset=CafeEmpaque.objects.all().order_by('empaque_cafe'), required=False, widget=forms.Select(attrs={'class': 'w-full select'}))
    origen = forms.ModelChoiceField(queryset=OrigenCafe.objects.all().order_by('origen'), required=False, widget=CodigoSourceSelect(codigo_attr='origen', attrs={'class': 'w-full select', 'data-codigo-source': 'origen', 'data-codigo-length': '3'}))
    proceso_inven_cafe = forms.ModelChoiceField(queryset=ProcesoInvenCafe.objects.all().order_by('proceso_inven_cafe'), required=False, widget=CodigoSourceSelect(codigo_attr='proceso_inven_cafe', attrs={'class': 'w-full select', 'data-codigo-source': 'proceso', 'data-codigo-length': '3'}))
    variendad_inven_cafe = forms.ModelChoiceField(queryset=VariedadCafe.objects.all().order_by('variedad_cafe', 'id'), required=False, widget=CodigoSourceSelect(codigo_attr='variedad_cafe', attrs={'class': 'w-full select', 'data-codigo-source': 'variedad', 'data-codigo-length': '3'}))

    class Meta:
        model = InventarioCafe
        fields = ['cliente', 'estado_cafe', 'origen', 'proceso_inven_cafe', 'variendad_inven_cafe', 'empaquecafe', 'codigo', 'descripcion', 'cantidad', 'sacos', 'cantidad_bolsas_emp', 'cantidad_paquetes']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'w-full input', 'readonly': 'readonly', 'maxlength': '26', 'autocomplete': 'off', 'data-auto-codigo': 'inventario-cafe'}),
            'descripcion': forms.TextInput(attrs={'class': 'w-full input'}),
            'cantidad': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'sacos': forms.NumberInput(attrs={'class': 'w-full input', 'step': '1', 'min': '0'}),
            'cantidad_bolsas_emp': forms.NumberInput(attrs={'class': 'w-full input', 'step': '1', 'min': '0'}),
            'cantidad_paquetes': forms.NumberInput(attrs={'class': 'w-full input', 'step': '1', 'min': '0'}),
        }

    required_field_names = [
        'cliente',
        'estado_cafe',
        'origen',
        'proceso_inven_cafe',
        'variendad_inven_cafe',
        'empaquecafe',
        'descripcion',
        'cantidad',
        'sacos',
        'cantidad_bolsas_emp',
        'cantidad_paquetes',
    ]

    def __init__(self, *args, enforce_required=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].required = False
        if enforce_required:
            for field_name in self.required_field_names:
                self.fields[field_name].required = True
                self.fields[field_name].error_messages['required'] = 'Este campo es obligatorio.'

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data = cleaned_data
        relation_fields = [
            'cliente',
            'estado_cafe',
            'origen',
            'proceso_inven_cafe',
            'variendad_inven_cafe',
        ]

        if any(field_name not in cleaned_data for field_name in relation_fields):
            return cleaned_data

        for field_name in relation_fields:
            setattr(self.instance, field_name, cleaned_data.get(field_name))

        codigo = self.instance.build_codigo()
        cleaned_data['codigo'] = codigo
        self.instance.codigo = codigo

        codigo_exists = InventarioCafe.objects.filter(codigo=codigo)
        if self.instance.pk:
            codigo_exists = codigo_exists.exclude(pk=self.instance.pk)

        if codigo_exists.exists():
            self.add_error('codigo', 'El código generado ya existe. Verifique los datos seleccionados.')

        return cleaned_data


@permiso_accion_requerido('inventario_cafe.view_inventariocafe', 'ver_inventario')
def listar_cafe(request):
    qs = (
        InventarioCafe.objects
        .select_related('cliente', 'estado_cafe', 'empaquecafe', 'origen', 'proceso_inven_cafe', 'variendad_inven_cafe')
        .only('id', 'cliente', 'estado_cafe', 'empaquecafe', 'origen', 'proceso_inven_cafe', 'variendad_inven_cafe', 'codigo', 'cantidad', 'sacos')
        .order_by('-id')
    )
    search = request.GET.get('q', '').strip()
    f_origen = request.GET.get('origen') or ''
    f_proceso = request.GET.get('proceso') or ''
    f_variedad = request.GET.get('variedad') or ''
    if search:
        if search.isdigit():
            qs = qs.filter(Q(id=int(search)) | Q(codigo__icontains=search))
        else:
            qs = qs.filter(
                Q(codigo__icontains=search) |
                Q(cliente__nombre__icontains=search) |
                Q(estado_cafe__estado_cafe__icontains=search) |
                Q(empaquecafe__empaque_cafe__icontains=search)
            )

    if f_origen.isdigit():
        qs = qs.filter(origen_id=int(f_origen))
    if f_proceso.isdigit():
        qs = qs.filter(proceso_inven_cafe_id=int(f_proceso))
    if f_variedad.isdigit():
        qs = qs.filter(variendad_inven_cafe_id=int(f_variedad))

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
        'origenes': OrigenCafe.objects.all().order_by('origen'),
        'procesos': ProcesoInvenCafe.objects.all().order_by('proceso_inven_cafe'),
        'variedades': VariedadCafe.objects.all().order_by('variedad_cafe', 'id'),
        'f_origen': f_origen,
        'f_proceso': f_proceso,
        'f_variedad': f_variedad,
    }
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'inventario_cafe/_modal_listar_Cafe.html', ctx)
    return render(request, 'inventario_cafe/listar_Cafe.html', ctx)


@require_http_methods(["GET","POST"])
@permiso_accion_requerido('inventario_cafe.add_inventariocafe', 'crear_inventario')
def add_cafe(request):
    if request.method == 'POST':
        print('POST crear inventario cafe:', request.POST)
        form = InventarioCafeForm(request.POST, enforce_required=True)
        form_valid = form.is_valid()
        print('FORM valid:', form_valid)
        print('FORM errors:', form.errors)
        if form_valid:
            try:
                obj = form.save(commit=False)
                # fecha_ingreso se usa solo para ordenar; no se muestra ni se ingresa
                if not obj.fecha_ingreso:
                    obj.fecha_ingreso = timezone.now()
                obj.created_at = timezone.now()
                obj.updated_at = timezone.now()
                obj.save()
                preserve = {k: (request.GET.get(k) or request.POST.get(k)) for k in ['q','origen','proceso','variedad','page'] if (request.GET.get(k) or request.POST.get(k))}
                if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                    qp = urlencode(preserve)
                    url = f"{reverse('inventario_cafe_listar')}?fragment=1" + (f"&{qp}" if qp else '')
                    return redirect(url)
                if preserve:
                    return redirect(f"{reverse('inventario_cafe_listar')}?{urlencode(preserve)}")
                return redirect('inventario_cafe_listar')
            except (ValidationError, DatabaseError, IntegrityError) as exc:
                print('SAVE crear inventario cafe error:', exc)
                form.add_error(None, f'No se pudo guardar el registro: {exc}')
    else:
        form = InventarioCafeForm()
    preserve = {k: request.GET.get(k) for k in ['q','origen','proceso','variedad','page'] if request.GET.get(k)}
    back_url = f"{reverse('inventario_cafe_listar')}?{urlencode(preserve)}" if preserve else reverse('inventario_cafe_listar')
    is_fragment = bool(request.headers.get('X-Fragment') or request.GET.get('fragment') == '1')
    # Variables individuales para plantillas (hidden inputs)
    ctx = {
        'form': form,
        'back_url': back_url,
        'is_fragment': is_fragment,
        'search': request.GET.get('q',''),
        'f_origen': request.GET.get('origen',''),
        'f_proceso': request.GET.get('proceso',''),
        'f_variedad': request.GET.get('variedad',''),
        'page_num': request.GET.get('page',''),
    }
    return render(request, 'inventario_cafe/add_Cafe.html', ctx)


@require_http_methods(["GET","POST"])
@permiso_accion_requerido('inventario_cafe.change_inventariocafe', 'editar_inventario')
def edit_cafe(request, pk):
    obj = get_object_or_404(InventarioCafe, pk=pk)
    if request.method == 'POST':
        form = InventarioCafeForm(request.POST, instance=obj)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.updated_at = timezone.now()
            inst.save()
            preserve = {k: (request.GET.get(k) or request.POST.get(k)) for k in ['q','origen','proceso','variedad','page'] if (request.GET.get(k) or request.POST.get(k))}
            if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                qp = urlencode(preserve)
                url = f"{reverse('inventario_cafe_listar')}?fragment=1" + (f"&{qp}" if qp else '')
                return redirect(url)
            if preserve:
                return redirect(f"{reverse('inventario_cafe_listar')}?{urlencode(preserve)}")
            return redirect('inventario_cafe_listar')
    else:
        form = InventarioCafeForm(instance=obj)
    preserve = {k: request.GET.get(k) for k in ['q','origen','proceso','variedad','page'] if request.GET.get(k)}
    back_url = f"{reverse('inventario_cafe_listar')}?{urlencode(preserve)}" if preserve else reverse('inventario_cafe_listar')
    is_fragment = bool(request.headers.get('X-Fragment') or request.GET.get('fragment') == '1')
    ctx = {
        'form': form,
        'obj': obj,
        'back_url': back_url,
        'is_fragment': is_fragment,
        'search': request.GET.get('q',''),
        'f_origen': request.GET.get('origen',''),
        'f_proceso': request.GET.get('proceso',''),
        'f_variedad': request.GET.get('variedad',''),
        'page_num': request.GET.get('page',''),
    }
    return render(request, 'inventario_cafe/detail_Cafe.html', ctx)


@permiso_accion_requerido('inventario_cafe.delete_inventariocafe', 'eliminar_inventario')
def delete_cafe(request, pk):
    obj = get_object_or_404(InventarioCafe, pk=pk)
    if request.method == 'POST':
        obj.delete()
        preserve = {k: (request.GET.get(k) or request.POST.get(k)) for k in ['q','origen','proceso','variedad','page'] if (request.GET.get(k) or request.POST.get(k))}
        if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
            qp = urlencode(preserve)
            url = f"{reverse('inventario_cafe_listar')}?fragment=1" + (f"&{qp}" if qp else '')
            return redirect(url)
        if preserve:
            return redirect(f"{reverse('inventario_cafe_listar')}?{urlencode(preserve)}")
        return redirect('inventario_cafe_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        ctx = {
            'obj': obj,
            'search': request.GET.get('q',''),
            'f_origen': request.GET.get('origen',''),
            'f_proceso': request.GET.get('proceso',''),
            'f_variedad': request.GET.get('variedad',''),
            'page_num': request.GET.get('page',''),
        }
        return render(request, 'inventario_cafe/confirm_delete_Cafe.html', ctx)
    return render(request, 'inventario_cafe/listar_Cafe.html', {})
