from django import forms
from django.core.exceptions import ValidationError

from .models import ProcesoInvenCafe


class ProcesoInvenCafeForm(forms.ModelForm):
    class Meta:
        model = ProcesoInvenCafe
        fields = ["proceso_inven_cafe"]
        widgets = {
            "proceso_inven_cafe": forms.TextInput(attrs={"class": "w-full input"}),
        }

    def clean_proceso_inven_cafe(self):
        proceso_raw = self.cleaned_data.get("proceso_inven_cafe") or ""
        proceso = proceso_raw.strip()
        normalizado = proceso.lower()

        if not normalizado:
            return proceso

        qs = ProcesoInvenCafe.objects.filter(proceso_inven_cafe__iexact=normalizado)
        if getattr(self.instance, "pk", None):
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("El proceso ya existe")

        return proceso
