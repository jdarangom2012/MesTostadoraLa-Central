
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Empleado
from .forms import EmpleadoForm
from django.core.paginator import Paginator
from django.db import IntegrityError, DatabaseError
from django.http import JsonResponse
def listar_empleados(request):
    search = request.GET.get('q', '').strip()
    empleados_list = Empleado.objects.all().order_by('-fecha_ingreso')
    if search:
        empleados_list = empleados_list.filter(
            identificacion__icontains=search
        )
    paginator = Paginator(empleados_list, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    ctx = {
        'empleados': page_obj.object_list,
        'page_obj': page_obj,
        'search': search
    }
    return render(request, 'empleados/_modal_listar_Empleados.html', ctx)

def add_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                from django.utils import timezone
                obj.fecha_ingreso = timezone.now()
                obj.save()
            except (IntegrityError, DatabaseError) as e:
                form.add_error(None, f'Error al guardar: {e}')
            else:
                messages.success(request, 'Empleado creado correctamente.')
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return listar_empleados(request)
                else:
                    return redirect('listar_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'empleados/add_Empleados.html', {'form': form})

def detail_empleado(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    if request.method == 'POST':
        if 'cancelar' in request.POST:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return listar_empleados(request)
            return redirect('listar_empleados')
        empleado.identificacion = request.POST.get('identificacion')
        empleado.nombres = request.POST.get('nombres')
        empleado.apellidos = request.POST.get('apellidos')
        empleado.estado = request.POST.get('estado')
        empleado.save()
        messages.success(request, 'Empleado actualizado exitosamente.')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return listar_empleados(request)
        return redirect('listar_empleados')
    return render(request, 'empleados/detail_Empleados.html', {'empleado': empleado})

def delete_empleado(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    if request.method == 'POST':
        empleado.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            return redirect('listar_empleados')
    return render(request, 'empleados/confirm_delete_Empleados.html', {'empleado': empleado})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Empleado

def detail_empleado(request, id):
    empleado = get_object_or_404(TblEmpleados, pk=id)


    if request.method == 'POST':
        if 'cancelar' in request.POST:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                from .views import listar_empleados
                return listar_empleados(request)
            return redirect('listar_empleados')

        # Guardar cambios
        empleado.identificacion = request.POST.get('identificacion')
        empleado.nombres = request.POST.get('nombres')
        empleado.apellidos = request.POST.get('apellidos')
        empleado.estado = request.POST.get('estado')
        empleado.save()
        messages.success(request, 'Empleado actualizado exitosamente.')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            from .views import listar_empleados
            return listar_empleados(request)
        return redirect('listar_empleados')

    return render(request, 'empleados/detail_Empleados.html', {'empleado': empleado})
from django.shortcuts import render, redirect
from django.contrib import messages

def add_empleado(request):
    if request.method == 'POST':
        identificacion = request.POST.get('identificacion')
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        estado = request.POST.get('estado')

        # Crear registro sin alterar fecha_ingreso (es GETDATE en la BD)
        Empleado.objects.create(
            identificacion=identificacion,
            nombres=nombres,
            apellidos=apellidos,
            estado=estado
        )
        messages.success(request, 'Empleado registrado exitosamente.')
        # Cerrar modal y actualizar listado
        return redirect('listar_empleados')

    return render(request, 'empleados/add_Empleados.html')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import EmpleadoForm
from django.core.paginator import Paginator
from django.db import IntegrityError, DatabaseError
from django.http import JsonResponse

@require_http_methods(["GET"])
def listar_empleados(request):
    search = request.GET.get('q', '').strip()
    empleados_list = Empleado.objects.all().order_by('-fecha_ingreso')
    if search:
        empleados_list = empleados_list.filter(
            identificacion__icontains=search
        )
    paginator = Paginator(empleados_list, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    ctx = {
        'empleados': page_obj.object_list,
        'page_obj': page_obj,
        'search': search
    }
    return render(request, 'empleados/_modal_listar_Empleados.html', ctx)

@require_http_methods(["GET", "POST"])
def add_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                from django.utils import timezone
                obj.fecha_ingreso = timezone.now()
                obj.save()
            except (IntegrityError, DatabaseError) as e:
                form.add_error(None, f'Error al guardar: {e}')
            else:
                messages.success(request, 'Empleado creado correctamente.')
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return listar_empleados(request)
                else:
                    return redirect('listar_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'empleados/add_Empleados.html', {'form': form})

@require_http_methods(["GET", "POST"])
def detail_empleado(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    if request.method == 'POST':
        if 'cancelar' in request.POST:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return listar_empleados(request)
            return redirect('listar_empleados')
        empleado.identificacion = request.POST.get('identificacion')
        empleado.nombres = request.POST.get('nombres')
        empleado.apellidos = request.POST.get('apellidos')
        empleado.estado = request.POST.get('estado')
        empleado.save()
        messages.success(request, 'Empleado actualizado exitosamente.')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return listar_empleados(request)
        return redirect('listar_empleados')
    return render(request, 'empleados/detail_Empleados.html', {'empleado': empleado})

@require_http_methods(["GET", "POST"])
def delete_empleado(request, id):
    empleado = get_object_or_404(TblEmpleados, pk=id)
    if request.method == 'POST':
        empleado.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            return redirect('listar_empleados')
    return render(request, 'empleados/confirm_delete_Empleados.html', {'empleado': empleado})
