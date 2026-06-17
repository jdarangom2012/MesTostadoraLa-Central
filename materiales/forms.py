from django import forms
from django.core.exceptions import ValidationError

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
    cliente = ClienteChoiceField(
        queryset=Cliente.objects.none(),
        required=False,
        widget=forms.Select(attrs={"class": "w-full select"}),
    )

    class Meta:
        model = Material
        fields = [
            "codigo_material",
            "descripcion",
            "cantidad",
            "estado",
            "cliente",
        ]
        widgets = {
            "codigo_material": forms.TextInput(attrs={"class": "w-full input"}),
            "descripcion": forms.TextInput(attrs={"class": "w-full input"}),
            "cantidad": forms.NumberInput(attrs={"class": "w-full input"}),
            "estado": forms.CheckboxInput(attrs={"class": "h-4 w-4"}),
            "fecha_ingreso": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "w-full input"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cliente_field = self.fields["cliente"]
        cliente_qs = Cliente.objects.all().order_by("apellidos", "nombre")
        cliente_field.queryset = cliente_qs
        cliente_field.empty_label = "Seleccione un cliente"

        choices = []
        for cliente in cliente_qs:
            nombre = (cliente.nombre or "").strip()
            apellidos = (cliente.apellidos or "").strip()
            label = (
                f"{apellidos}, {nombre}"
                if apellidos and nombre
                else (apellidos or nombre) or f"Cliente {cliente.pk}"
            )
            choices.append((cliente.pk, label))
        cliente_field.choices = [("", cliente_field.empty_label)] + choices

    def clean_codigo_material(self):
        codigo = (self.cleaned_data.get("codigo_material") or "").strip()
        if not codigo:
            return codigo

        qs = Material.objects.filter(codigo_material__iexact=codigo)
        if getattr(self.instance, "pk", None):
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("El código ya existe")

        return codigo
