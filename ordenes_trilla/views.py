from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms
import re
from .models import OrdenTrilla
from ordenes.models import Orden
from estado_tareas.models import EstadoTarea


class OrdenChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        oid = getattr(obj, 'id', None) or getattr(obj, 'pk', '')
        return f"Orden {oid}"


class OrdenTrillaForm(forms.ModelForm):
    orden = OrdenChoiceField(queryset=Orden.objects.none(), required=False, widget=forms.Select(attrs={'class':'w-full select'}))
    estado_tareas = forms.ModelChoiceField(queryset=EstadoTarea.objects.all().order_by('estado_tareas'), required=False, widget=forms.Select(attrs={'class':'w-full select'}))

    class Meta:
        model = OrdenTrilla
        # fecha_ingreso es automática; no se expone en el formulario
        fields = ['orden','estado_tareas','peso_cafe_bruto','peso_cafe_verde','rendimiento']
        widgets = {
            'peso_cafe_bruto': forms.NumberInput(attrs={'class':'w-full input', 'step':'0.01'}),
            'peso_cafe_verde': forms.NumberInput(attrs={'class':'w-full input', 'step':'0.01'}),
            'rendimiento': forms.NumberInput(attrs={'class':'w-full input', 'step':'0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Órdenes: cuando está ligado (POST), permitir cualquier orden para evitar errores de validación
        base_qs = Orden.objects.all().order_by('-id')
        if self.is_bound:
            # Evita "Escoja una opción válida" aunque la orden no esté en el top N
            self.fields['orden'].queryset = base_qs
        else:
            # En carga inicial, limitar para rendimiento
            self.fields['orden'].queryset = base_qs.select_related('cliente')[:200]
        self.fields['orden'].empty_label = 'Seleccione una orden'


@permission_required('ordenes_trilla.view_ordentrilla', raise_exception=True)
def listar_ordenes_trilla(request):
    qs = OrdenTrilla.objects.select_related('orden__cliente','estado_tareas')
    search = request.GET.get('q','').strip()
    if search:
        s = search.strip()
        filters = (
            Q(orden__cliente__nombre__icontains=s) |
            Q(orden__cliente__apellidos__icontains=s)
        )
        # Soportar texto completo como "Orden 6" o el número aislado "6"
        m = re.search(r"(?:^|\b)orden\s*(\d+)\b", s, flags=re.IGNORECASE)
        if m:
            try:
                filters |= Q(orden__id=int(m.group(1)))
            except ValueError:
                pass
        else:
            # Si no hay patrón "Orden N", pero hay un número en el término, úsalo
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
        'trillas': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'search': search,
    }
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'ordenes_trilla/_modal_listar_OrdenesTrilla.html', ctx)
    return render(request, 'ordenes_trilla/listar_OrdenesTrilla.html', ctx)


@require_http_methods(["GET","POST"])
@permission_required('ordenes_trilla.add_ordentrilla', raise_exception=True)
def add_orden_trilla(request):
    if request.method == 'POST':
        form = OrdenTrillaForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            from django.utils import timezone
            # Fecha de ingreso automática
            obj.fecha_ingreso = timezone.now()
            obj.created_at = timezone.now()
            obj.updated_at = timezone.now()
            obj.save()
            if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                return listar_ordenes_trilla(request)
            return redirect('ordenes_trilla_listar')
    else:
        form = OrdenTrillaForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'ordenes_trilla/add_OrdenesTrilla.html', {'form': form})
    return render(request, 'ordenes_trilla/listar_OrdenesTrilla.html', {})


@require_http_methods(["GET","POST"])
@permission_required('ordenes_trilla.change_ordentrilla', raise_exception=True)
def edit_orden_trilla(request, pk):
    trilla = get_object_or_404(OrdenTrilla, pk=pk)
    if request.method == 'POST':
        form = OrdenTrillaForm(request.POST, instance=trilla)
        if form.is_valid():
            obj = form.save(commit=False)
            from django.utils import timezone
            obj.updated_at = timezone.now()
            obj.save()
            if request.headers.get('X-Fragment'):
                return listar_ordenes_trilla(request)
            return redirect('ordenes_trilla_listar')
    else:
        form = OrdenTrillaForm(instance=trilla)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'ordenes_trilla/detail_OrdenesTrilla.html', {'form': form, 'trilla': trilla})
    return render(request, 'ordenes_trilla/listar_OrdenesTrilla.html', {})


@permission_required('ordenes_trilla.delete_ordentrilla', raise_exception=True)
def delete_orden_trilla(request, pk):
    t = get_object_or_404(OrdenTrilla, pk=pk)
    if request.method == 'POST':
        t.delete()
        if request.headers.get('X-Fragment'):
            return listar_ordenes_trilla(request)
        return redirect('ordenes_trilla_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'ordenes_trilla/confirm_delete_OrdenesTrilla.html', {'t': t})
    return render(request, 'ordenes_trilla/listar_OrdenesTrilla.html', {})
