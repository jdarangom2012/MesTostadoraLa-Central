from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms
import re

from .models import SeleccionTueste
from ordenes.models import Orden
from estado_tareas.models import EstadoTarea


class OrdenChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        try:
            return str(obj)
        except Exception:
            return f"Orden {getattr(obj, 'pk', '')}"


class SeleccionTuesteForm(forms.ModelForm):
    orden = OrdenChoiceField(queryset=Orden.objects.none(), required=False, widget=forms.Select(attrs={'class':'w-full select'}))
    estado_tareas = forms.ModelChoiceField(queryset=EstadoTarea.objects.all().order_by('estado_tareas'), required=False, widget=forms.Select(attrs={'class':'w-full select'}))

    class Meta:
        model = SeleccionTueste
        fields = [
            'orden','estado_tareas',
            'cat_limpieza','cat_quaker','peso_quaker',
            'cat_grupo1','desc_grupo1','peso_grupo1',
            'cat_grupo2','desc_grupo2','peso_grupo2',
            'cat_grupo3','desc_grupo3','peso_grupo3',
        ]
        widgets = {
            'cat_limpieza': forms.CheckboxInput(attrs={'class':'toggle'}),
            'cat_quaker': forms.CheckboxInput(attrs={'class':'toggle'}),
            'peso_quaker': forms.NumberInput(attrs={'class':'w-full input','step':'0.01'}),
            'cat_grupo1': forms.CheckboxInput(attrs={'class':'toggle'}),
            'desc_grupo1': forms.TextInput(attrs={'class':'w-full input'}),
            'peso_grupo1': forms.NumberInput(attrs={'class':'w-full input','step':'0.01'}),
            'cat_grupo2': forms.CheckboxInput(attrs={'class':'toggle'}),
            'desc_grupo2': forms.TextInput(attrs={'class':'w-full input'}),
            'peso_grupo2': forms.NumberInput(attrs={'class':'w-full input','step':'0.01'}),
            'cat_grupo3': forms.CheckboxInput(attrs={'class':'toggle'}),
            'desc_grupo3': forms.TextInput(attrs={'class':'w-full input'}),
            'peso_grupo3': forms.NumberInput(attrs={'class':'w-full input','step':'0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_qs = Orden.objects.all().order_by('-id')
        if self.is_bound:
            self.fields['orden'].queryset = base_qs
        else:
            self.fields['orden'].queryset = base_qs.select_related('cliente')[:200]
        self.fields['orden'].empty_label = 'Seleccione una orden'


@permission_required('seleccion_tueste.view_selecciontueste', raise_exception=True)
def listar_ordenes_seleccion_tueste(request):
    qs = (
        SeleccionTueste.objects
        .select_related('orden__cliente', 'estado_tareas')
        .only(
            'id', 'orden', 'estado_tareas',
            'cat_limpieza', 'cat_quaker', 'peso_quaker',
            'cat_grupo1', 'desc_grupo1', 'peso_grupo1',
            'cat_grupo2', 'desc_grupo2', 'peso_grupo2',
            'cat_grupo3', 'desc_grupo3', 'peso_grupo3',
        )
    )
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
        'selecciones': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'search': search,
    }
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'seleccion_tueste/_modal_listar_OrdenesSeleccionTueste.html', ctx)
    return render(request, 'seleccion_tueste/listar_OrdenesSeleccionTueste.html', ctx)


@require_http_methods(["GET","POST"])
@permission_required('seleccion_tueste.add_selecciontueste', raise_exception=True)
def add_orden_seleccion_tueste(request):
    if request.method == 'POST':
        form = SeleccionTuesteForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            from django.utils import timezone
            if not obj.fecha_ingreso:
                obj.fecha_ingreso = timezone.now()
            obj.created_at = timezone.now()
            obj.updated_at = timezone.now()
            obj.save()
            if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                return listar_ordenes_seleccion_tueste(request)
            return redirect('ordenes_seleccion_tueste_listar')
    else:
        form = SeleccionTuesteForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'seleccion_tueste/add_OrdenesSeleccionTueste.html', {'form': form})
    return render(request, 'seleccion_tueste/listar_OrdenesSeleccionTueste.html', {})


@require_http_methods(["GET","POST"])
@permission_required('seleccion_tueste.change_selecciontueste', raise_exception=True)
def edit_orden_seleccion_tueste(request, pk):
    obj = get_object_or_404(SeleccionTueste, pk=pk)
    if request.method == 'POST':
        form = SeleccionTuesteForm(request.POST, instance=obj)
        if form.is_valid():
            inst = form.save(commit=False)
            from django.utils import timezone
            inst.updated_at = timezone.now()
            inst.save()
            if request.headers.get('X-Fragment'):
                return listar_ordenes_seleccion_tueste(request)
            return redirect('ordenes_seleccion_tueste_listar')
    else:
        form = SeleccionTuesteForm(instance=obj)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'seleccion_tueste/detail_OrdenesSeleccionTueste.html', {'form': form, 'obj': obj})
    return render(request, 'seleccion_tueste/listar_OrdenesSeleccionTueste.html', {})


@permission_required('seleccion_tueste.delete_selecciontueste', raise_exception=True)
def delete_orden_seleccion_tueste(request, pk):
    obj = get_object_or_404(SeleccionTueste, pk=pk)
    if request.method == 'POST':
        obj.delete()
        if request.headers.get('X-Fragment'):
            return listar_ordenes_seleccion_tueste(request)
        return redirect('ordenes_seleccion_tueste_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'seleccion_tueste/confirm_delete_OrdenesSeleccionTueste.html', {'t': obj})
    return render(request, 'seleccion_tueste/listar_OrdenesSeleccionTueste.html', {})
