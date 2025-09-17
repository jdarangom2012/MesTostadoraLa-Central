from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms
from .models import Material
from clientes.models import Cliente


class ClienteChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        nombre = (getattr(obj, 'nombre', '') or '').strip()
        apellidos = (getattr(obj, 'apellidos', '') or '').strip()
        if apellidos and nombre:
            return f"{apellidos}, {nombre}"
        return apellidos or nombre or f"Cliente {getattr(obj, 'id', '')}"


class MaterialForm(forms.ModelForm):
    cliente = ClienteChoiceField(queryset=Cliente.objects.none(), required=False, widget=forms.Select(attrs={'class': 'w-full select'}))
    class Meta:
        model = Material
        fields = [
            'codigo_material','descripcion','cantidad','estado','cliente'
        ]
        widgets = {
            'codigo_material': forms.TextInput(attrs={'class': 'w-full input'}),
            'descripcion': forms.TextInput(attrs={'class': 'w-full input'}),
            'cantidad': forms.NumberInput(attrs={'class': 'w-full input'}),
            'estado': forms.CheckboxInput(attrs={'class': 'h-4 w-4'}),
            'fecha_ingreso': forms.DateTimeInput(attrs={'type':'datetime-local','class':'w-full input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Poblamos el combo de clientes ordenado por nombre y apellidos y con placeholder
        cliente_field = self.fields['cliente']
        cliente_qs = Cliente.objects.all().order_by('apellidos', 'nombre')
        cliente_field.queryset = cliente_qs
        cliente_field.empty_label = 'Seleccione un cliente'
        # Fuerza etiquetas "Nombre Apellidos" en el combo
        choices = []
        for c in cliente_qs:
            n = (c.nombre or '').strip()
            a = (c.apellidos or '').strip()
            label = f"{a}, {n}" if a and n else (a or n) or f"Cliente {c.pk}"
            choices.append((c.pk, label))
        cliente_field.choices = [('', cliente_field.empty_label)] + choices


@permission_required('materiales.view_material', raise_exception=True)
def listar_materiales(request):
    qs = Material.objects.select_related('cliente')
    search = request.GET.get('q', '').strip()
    if search:
        qs = qs.filter(
            Q(codigo_material__icontains=search) |
            Q(descripcion__icontains=search)
        )
    qs = qs.order_by('descripcion','id')

    paginator = Paginator(qs, 7)
    page = request.GET.get('page')
    try:
        materiales_page = paginator.page(page)
    except PageNotAnInteger:
        materiales_page = paginator.page(1)
    except EmptyPage:
        materiales_page = paginator.page(paginator.num_pages)

    ctx = {
        'materiales': materiales_page,
        'page_obj': materiales_page,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'search': search,
    }
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'materiales/_modal_listar_materiales.html', ctx)
    return render(request, 'materiales/listar_Materiales.html', ctx)


@require_http_methods(["GET","POST"])
@permission_required('materiales.add_material', raise_exception=True)
def add_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            from django.utils import timezone
            obj.created_at = timezone.now()
            obj.updated_at = timezone.now()
            if not obj.fecha_ingreso:
                obj.fecha_ingreso = timezone.now()
            try:
                obj.save()
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                    return listar_materiales(request)
                return redirect('materiales_listar')
    else:
        form = MaterialForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'materiales/add_Materiales.html', {'form': form})
    return render(request, 'materiales/listar_Materiales.html', {})


@require_http_methods(["GET","POST"])
@permission_required('materiales.change_material', raise_exception=True)
def edit_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            obj = form.save(commit=False)
            from django.utils import timezone
            obj.updated_at = timezone.now()
            try:
                obj.save()
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment'):
                    return listar_materiales(request)
                return redirect('materiales_listar')
    else:
        form = MaterialForm(instance=material)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'materiales/detail_Materiales.html', {'form': form, 'material': material})
    return render(request, 'materiales/listar_Materiales.html', {})


@permission_required('materiales.delete_material', raise_exception=True)
def delete_material(request, pk):
    m = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        m.delete()
        if request.headers.get('X-Fragment'):
            return listar_materiales(request)
        return redirect('materiales_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'materiales/confirm_delete_material.html', {'m': m})
    return render(request, 'materiales/listar_Materiales.html', {})
