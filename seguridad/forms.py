from django import forms

from .models import Modulo, Permiso, PermisoCampo, Rol


class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full input'}),
            'descripcion': forms.Textarea(attrs={'class': 'w-full input', 'rows': 3}),
        }


class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permiso
        fields = ['codigo', 'descripcion']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'w-full input'}),
            'descripcion': forms.TextInput(attrs={'class': 'w-full input'}),
        }


class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = ['nombre', 'url', 'icono', 'orden']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full input'}),
            'url': forms.TextInput(attrs={'class': 'w-full input'}),
            'icono': forms.TextInput(attrs={'class': 'w-full input'}),
            'orden': forms.NumberInput(attrs={'class': 'w-full input'}),
        }


class PermisoCampoForm(forms.ModelForm):
    class Meta:
        model = PermisoCampo
        fields = ['rol', 'modelo', 'campo', 'puede_ver', 'puede_editar']
        widgets = {
            'rol': forms.Select(attrs={'class': 'w-full input'}),
            'modelo': forms.TextInput(attrs={'class': 'w-full input', 'placeholder': 'app_label.ModelName'}),
            'campo': forms.TextInput(attrs={'class': 'w-full input', 'placeholder': 'nombre_campo'}),
            'puede_ver': forms.CheckboxInput(attrs={'class': 'h-4 w-4'}),
            'puede_editar': forms.CheckboxInput(attrs={'class': 'h-4 w-4'}),
        }
