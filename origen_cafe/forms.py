from django import forms
from django.core.exceptions import ValidationError

from .models import OrigenCafe


class OrigenCafeForm(forms.ModelForm):
    class Meta:
        model = OrigenCafe
        fields = ["origen"]
        widgets = {
            "origen": forms.TextInput(attrs={"class": "w-full input"}),
        }

    def clean_origen(self):
        origen_raw = self.cleaned_data.get("origen") or ""
        origen = origen_raw.strip()
        normalizado = origen.lower()

        if not normalizado:
            return origen

        qs = OrigenCafe.objects.filter(origen__iexact=normalizado)
        if getattr(self.instance, "pk", None):
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("El origen ya existe")

        return origen
