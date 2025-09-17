from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms
import re

from .models import Tueste
from ordenes.models import Orden
from estado_tareas.models import EstadoTarea
from nivel_tueste.models import NivelTueste
from inventario_cafe.models import InventarioCafe


class OrdenChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        oid = getattr(obj, 'id', None) or getattr(obj, 'pk', '')
        return f"Orden {oid}"


class InventarioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.codigo or f"INV-{obj.id:06d}"


class TuesteForm(forms.ModelForm):
    orden = OrdenChoiceField(queryset=Orden.objects.none(), required=False, widget=forms.Select(attrs={'class':'w-full select'}))
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
            'rendimiento': forms.NumberInput(attrs={'class':'w-full input', 'step':'0.01'}),
            'peso_cafe_vede_total': forms.NumberInput(attrs={'class':'w-full input', 'step':'0.01'}),
            'peso_cafe_tostado_total': forms.NumberInput(attrs={'class':'w-full input', 'step':'0.01'}),
            'notas': forms.TextInput(attrs={'class':'w-full input'}),
            'notas_op': forms.TextInput(attrs={'class':'w-full input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_qs = Orden.objects.all().order_by('-id')
        if self.is_bound:
            self.fields['orden'].queryset = base_qs
        else:
            self.fields['orden'].queryset = base_qs.select_related('cliente')[:200]
        self.fields['orden'].empty_label = 'Seleccione una orden'
        self.fields['inventario_cafe_ref'].empty_label = 'Seleccione un café'


@permission_required('tueste.view_tueste', raise_exception=True)
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

    ctx = {
        'tuestes': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'search': search,
    }
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'tueste/_modal_listar_OrdenesTueste.html', ctx)
    return render(request, 'tueste/listar_OrdenesTueste.html', ctx)


@require_http_methods(["GET","POST"])
@permission_required('tueste.add_tueste', raise_exception=True)
def add_orden_tueste(request):
    if request.method == 'POST':
        form = TuesteForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            from django.utils import timezone
            obj.fecha_ingreso = timezone.now()
            obj.created_at = timezone.now()
            obj.updated_at = timezone.now()
            obj.save()
            if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                return listar_ordenes_tueste(request)
            return redirect('ordenes_tueste_listar')
    else:
        form = TuesteForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'tueste/add_OrdenesTueste.html', {'form': form})
    return render(request, 'tueste/listar_OrdenesTueste.html', {})


@require_http_methods(["GET","POST"])
@permission_required('tueste.change_tueste', raise_exception=True)
def edit_orden_tueste(request, pk):
    tueste = get_object_or_404(Tueste, pk=pk)
    if request.method == 'POST':
        form = TuesteForm(request.POST, instance=tueste)
        if form.is_valid():
            obj = form.save(commit=False)
            from django.utils import timezone
            obj.updated_at = timezone.now()
            obj.save()
            if request.headers.get('X-Fragment'):
                return listar_ordenes_tueste(request)
            return redirect('ordenes_tueste_listar')
    else:
        form = TuesteForm(instance=tueste)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'tueste/detail_OrdenesTueste.html', {'form': form, 'tueste': tueste})
    return render(request, 'tueste/listar_OrdenesTueste.html', {})


@permission_required('tueste.delete_tueste', raise_exception=True)
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
