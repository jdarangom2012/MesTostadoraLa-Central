from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Cliente
from django import forms


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'codigo','nombre','apellidos','telefono','direccion','email',
            'id_tipo_cliente','id_tipo_identificacion','id_estado_cliente'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'w-full input'}),
            'nombre': forms.TextInput(attrs={'class': 'w-full input'}),
            'apellidos': forms.TextInput(attrs={'class': 'w-full input'}),
            'telefono': forms.TextInput(attrs={'class': 'w-full input'}),
            'direccion': forms.TextInput(attrs={'class': 'w-full input'}),
            'email': forms.EmailInput(attrs={'class': 'w-full input'}),
            'id_tipo_cliente': forms.Select(attrs={'class': 'w-full select'}),
            'id_tipo_identificacion': forms.Select(attrs={'class': 'w-full select'}),
            'id_estado_cliente': forms.Select(attrs={'class': 'w-full select'}),
        }


@permission_required('clientes.view_cliente', raise_exception=True)
def listar_clientes(request):
    qs = Cliente.objects.select_related('id_tipo_cliente','id_estado_cliente')
    search = request.GET.get('q','').strip()
    if search:
        qs = qs.filter(
            Q(nombre__icontains=search) |
            Q(apellidos__icontains=search) |
            Q(codigo__icontains=search)
        )
    qs = qs.order_by('nombre','apellidos','id')

    paginator = Paginator(qs, 7)
    page = request.GET.get('page')
    try:
        clientes_page = paginator.page(page)
    except PageNotAnInteger:
        clientes_page = paginator.page(1)
    except EmptyPage:
        clientes_page = paginator.page(paginator.num_pages)

    ctx = {
        'clientes': clientes_page,
        'page_obj': clientes_page,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'search': search,
    }
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'clientes/_modal_listar_clientes.html', ctx)
    return render(request, 'clientes/listar_clientes.html', ctx)


@require_http_methods(["GET","POST"])
@permission_required('clientes.add_cliente', raise_exception=True)
def add_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            from django.utils import timezone
            obj.created_at = timezone.now()
            obj.save()
            if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                return listar_clientes(request)
            return redirect('clientes_listar')
    else:
        form = ClienteForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'clientes/add_clientes.html', {'form': form})
    return render(request, 'clientes/listar_clientes.html', {})


@permission_required('clientes.delete_cliente', raise_exception=True)
def delete_cliente(request, pk):
    c = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        c.delete()
        if request.headers.get('X-Fragment'):
            # tras eliminar devolvemos listado actualizado
            return listar_clientes(request)
        return redirect('clientes_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'clientes/confirm_delete_cliente.html', {'c': c})
    return render(request, 'clientes/listar_clientes.html', {})  # fallback simple


@require_http_methods(["GET","POST"])
@permission_required('clientes.change_cliente', raise_exception=True)
def edit_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            obj = form.save(commit=False)
            from django.utils import timezone
            obj.updated_at = timezone.now()
            obj.save()
            if request.headers.get('X-Fragment'):
                return listar_clientes(request)
            return redirect('clientes_listar')
    else:
        form = ClienteForm(instance=cliente)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'clientes/detail_clientes.html', {'form': form, 'cliente': cliente})
    return render(request, 'clientes/listar_clientes.html', {})
