from django import forms
from django.core.exceptions import ValidationError

from .models import EstadoCafe


class EstadoForm(forms.ModelForm):
    class Meta:
        model = EstadoCafe
        fields = ["estado_cafe"]
        widgets = {
            "estado_cafe": forms.TextInput(attrs={"class": "w-full input"}),
        }

    def clean_estado_cafe(self):
        estado_raw = self.cleaned_data.get("estado_cafe") or ""
        estado = estado_raw.strip()
        normalizado = estado.lower()

        if not normalizado:
            return estado

        qs = EstadoCafe.objects.filter(estado_cafe__iexact=normalizado)
        if getattr(self.instance, "pk", None):
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("Estado del café ya existe")

        return estado
