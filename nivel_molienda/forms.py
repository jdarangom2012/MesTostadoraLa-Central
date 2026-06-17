from django import forms
from django.core.exceptions import ValidationError

from .models import NivelMolienda


class NivelMoliendaForm(forms.ModelForm):
    class Meta:
        model = NivelMolienda
        fields = ["nivel_molienda"]
        widgets = {
            "nivel_molienda": forms.TextInput(attrs={"class": "w-full input"}),
        }

    def clean_nivel_molienda(self):
        nivel_raw = self.cleaned_data.get("nivel_molienda") or ""
        nivel = nivel_raw.strip()
        normalizado = nivel.lower()

        if not normalizado:
            return nivel

        qs = NivelMolienda.objects.filter(nivel_molienda__iexact=normalizado)
        if getattr(self.instance, "pk", None):
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("El nivel de molienda ya existe")

        return nivel
