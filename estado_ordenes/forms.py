from django import forms
from django.core.exceptions import ValidationError

from .models import EstadoOrden


class EstadoOrdenForm(forms.ModelForm):
    class Meta:
        model = EstadoOrden
        fields = ["estado_orden"]
        widgets = {
            "estado_orden": forms.TextInput(attrs={"class": "w-full input"}),
        }

    def clean_estado_orden(self):
        estado_raw = self.cleaned_data.get("estado_orden") or ""
        estado = estado_raw.strip()
        normalizado = estado.lower()

        if not normalizado:
            return estado

        qs = EstadoOrden.objects.filter(estado_orden__iexact=normalizado)
        if getattr(self.instance, "pk", None):
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("Estado de la Orden ya existe")

        return estado
