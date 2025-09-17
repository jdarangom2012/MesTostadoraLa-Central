from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms
from django.utils import timezone

from .models import OrdenSeleccionVerde
from estado_tareas.models import EstadoTarea


class OrdenSeleccionVerdeForm(forms.ModelForm):
    estado_tareas = forms.ModelChoiceField(
        queryset=EstadoTarea.objects.all().order_by('estado_tareas'),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full select'})
    )

    class Meta:
        model = OrdenSeleccionVerde
        fields = [
            'estado_tareas',
            'zaranda',
            'grupo1','peso_grupo1',
            'grupo2','peso_grupo2',
            'grupo3','peso_grupo3',
            'grupo4','peso_grupo4',
            'grupo5','peso_grupo5',
            'peso_grupo_ripio',
            'catadora',
            'catacion_ripio','peso_cat_ripio',
            'catacion_balsos','peso_cat_balsos',
            'catacion_grupo1','peso_cat_grupo1',
            'catacion_grupo2','peso_cat_grupo2',
            'peso_aceptado',
            'medir_humedad','humedad',
            'medir_densidad','densidad',
        ]
        widgets = {
            'zaranda': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'grupo1': forms.TextInput(attrs={'class': 'w-full input'}),
            'peso_grupo1': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'grupo2': forms.TextInput(attrs={'class': 'w-full input'}),
            'peso_grupo2': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'grupo3': forms.TextInput(attrs={'class': 'w-full input'}),
            'peso_grupo3': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'grupo4': forms.TextInput(attrs={'class': 'w-full input'}),
            'peso_grupo4': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'grupo5': forms.TextInput(attrs={'class': 'w-full input'}),
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
        }


@permission_required('ordenes_seleccion_verde.view_ordenseleccionverde', raise_exception=True)
def listar_ordenes_seleccion_verde(request):
    qs = (
        OrdenSeleccionVerde.objects
        .select_related('estado_tareas')
        .only(
            'id','estado_tareas',
            'zaranda','peso_aceptado','humedad','densidad',
        )
        .order_by('-fecha_ingreso','-id')
    )
    search = request.GET.get('q', '').strip()
    if search:
        if search.isdigit():
            qs = qs.filter(id=int(search))
        else:
            qs = qs.filter(
                Q(estado_tareas__estado_tareas__icontains=search) |
                Q(grupo1__icontains=search) | Q(grupo2__icontains=search) |
                Q(grupo3__icontains=search) | Q(grupo4__icontains=search) |
                Q(grupo5__icontains=search)
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
        return render(request, 'ordenes_seleccion_verde/_modal_listar_OrdenesSelecionVerde.html', ctx)
    return render(request, 'ordenes_seleccion_verde/listar_OrdenesSelecionVerde.html', ctx)


@require_http_methods(["GET","POST"])
@permission_required('ordenes_seleccion_verde.add_ordenseleccionverde', raise_exception=True)
def add_orden_seleccion_verde(request):
    if request.method == 'POST':
        form = OrdenSeleccionVerdeForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.fecha_ingreso:
                obj.fecha_ingreso = timezone.now()
            obj.created_at = timezone.now()
            obj.updated_at = timezone.now()
            obj.save()
            if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                return listar_ordenes_seleccion_verde(request)
            return redirect('ordenes_seleccion_verde_listar')
    else:
        form = OrdenSeleccionVerdeForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'ordenes_seleccion_verde/add_OrdenesSelecionVerde.html', {'form': form})
    return render(request, 'ordenes_seleccion_verde/listar_OrdenesSelecionVerde.html', {})


@require_http_methods(["GET","POST"])
@permission_required('ordenes_seleccion_verde.change_ordenseleccionverde', raise_exception=True)
def edit_orden_seleccion_verde(request, pk):
    obj = get_object_or_404(OrdenSeleccionVerde, pk=pk)
    if request.method == 'POST':
        form = OrdenSeleccionVerdeForm(request.POST, instance=obj)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.updated_at = timezone.now()
            inst.save()
            if request.headers.get('X-Fragment'):
                return listar_ordenes_seleccion_verde(request)
            return redirect('ordenes_seleccion_verde_listar')
    else:
        form = OrdenSeleccionVerdeForm(instance=obj)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'ordenes_seleccion_verde/detail_OrdenesSelecionVerde.html', {'form': form, 'obj': obj})
    return render(request, 'ordenes_seleccion_verde/listar_OrdenesSelecionVerde.html', {})


@permission_required('ordenes_seleccion_verde.delete_ordenseleccionverde', raise_exception=True)
def delete_orden_seleccion_verde(request, pk):
    obj = get_object_or_404(OrdenSeleccionVerde, pk=pk)
    if request.method == 'POST':
        obj.delete()
        if request.headers.get('X-Fragment'):
            return listar_ordenes_seleccion_verde(request)
        return redirect('ordenes_seleccion_verde_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'ordenes_seleccion_verde/confirm_delete_OrdenesSelecionVerde.html', {'t': obj})
    return render(request, 'ordenes_seleccion_verde/listar_OrdenesSelecionVerde.html', {})
