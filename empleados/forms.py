from django import forms
from .models import Empleado, EstadoEmpleado


FIELD_CSS_CLASS = 'field-input w-full rounded-lg border border-brand-dark/50 bg-brand-light px-3 py-2 text-sm text-brand-dark placeholder-brand-dark/50 focus:outline-none focus:ring-2 focus:ring-brand-primary/70 focus:border-brand-primary'

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['identificacion', 'nombres', 'apellidos', 'estado']
        labels = {
            'estado': 'Estado',
        }
        widgets = {
            'identificacion': forms.TextInput(attrs={'class': FIELD_CSS_CLASS, 'placeholder': 'Identificación'}),
            'nombres': forms.TextInput(attrs={'class': FIELD_CSS_CLASS, 'placeholder': 'Nombres'}),
            'apellidos': forms.TextInput(attrs={'class': FIELD_CSS_CLASS, 'placeholder': 'Apellidos'}),
            'estado': forms.Select(attrs={'class': FIELD_CSS_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].queryset = EstadoEmpleado.objects.order_by('Estado')
        self.fields['estado'].empty_label = 'Seleccione un estado'
        self.fields['estado'].label = 'Estado'

    def clean_identificacion(self):
        identificacion = self.cleaned_data.get('identificacion')
        if not identificacion:
            raise forms.ValidationError('La identificación es obligatoria.')
        identificacion = str(identificacion).strip()

        qs = Empleado.objects.filter(identificacion__iexact=identificacion)
        if self.instance and getattr(self.instance, 'pk', None):
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('El empleado ya existe')

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
