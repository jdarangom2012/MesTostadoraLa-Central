from django import forms
from django.core.exceptions import ValidationError

from .models import CafeEmpaque


class CafeEmpaqueForm(forms.ModelForm):
    class Meta:
        model = CafeEmpaque
        fields = ["empaque_cafe"]
        widgets = {
            "empaque_cafe": forms.TextInput(attrs={"class": "w-full input"}),
        }

    def clean_empaque_cafe(self):
        empaque_raw = self.cleaned_data.get("empaque_cafe") or ""
        empaque = empaque_raw.strip()
        normalizado = empaque.lower()

        if not normalizado:
            return empaque

        qs = CafeEmpaque.objects.filter(empaque_cafe__iexact=normalizado)
        if getattr(self.instance, "pk", None):
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("El empaque ya existe")

        return empaque
