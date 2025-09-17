from django.db import models


class OptimizedQuerysetMixin:
    """Mixin para aplicar select_related/prefetch_related estándar.

    Define atributos opcionales en el viewset:
      select_related_fields = []
      prefetch_related_fields = []
    """

    select_related_fields: list[str] = []
    prefetch_related_fields: list[str] = []

    def get_queryset(self):
        qs = super().get_queryset()
        if self.select_related_fields:
            qs = qs.select_related(*self.select_related_fields)
        if self.prefetch_related_fields:
            qs = qs.prefetch_related(*self.prefetch_related_fields)
        return qs