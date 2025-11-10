from django import forms
from .models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        exclude = ['fecha_ingreso']
        widgets = {
            'identificacion': forms.TextInput(attrs={'class': 'input w-full', 'placeholder': 'Identificación'}),
            'nombres': forms.TextInput(attrs={'class': 'input w-full', 'placeholder': 'Nombres'}),
            'apellidos': forms.TextInput(attrs={'class': 'input w-full', 'placeholder': 'Apellidos'}),
            'estado': forms.TextInput(attrs={'class': 'input w-full', 'placeholder': 'Estado'}),
        }

    def clean_identificacion(self):
        identificacion = self.cleaned_data.get('identificacion')
        if not identificacion:
            raise forms.ValidationError('La identificación es obligatoria.')
        return identificacion

    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres')
        if not nombres:
            raise forms.ValidationError('El nombre es obligatorio.')
        return nombres

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if not apellidos:
            raise forms.ValidationError('El apellido es obligatorio.')
        return apellidos
