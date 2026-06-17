from django import forms
from django.core.exceptions import ValidationError

from .models import VariendadInvenCafe


class VariendadInvenCafeForm(forms.ModelForm):
    class Meta:
        model = VariendadInvenCafe
        fields = ["variedad_inven_cafe"]
        widgets = {
            "variedad_inven_cafe": forms.TextInput(attrs={"class": "w-full input"}),
        }

    def clean_variedad_inven_cafe(self):
        variedad_raw = self.cleaned_data.get("variedad_inven_cafe") or ""
        variedad = variedad_raw.strip()
        normalizado = variedad.lower()

        if not normalizado:
            return variedad

        qs = VariendadInvenCafe.objects.filter(variedad_inven_cafe__iexact=normalizado)
        if getattr(self.instance, "pk", None):
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("La variedad ya existe")

        return variedad