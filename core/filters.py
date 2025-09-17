from rest_framework.filters import SearchFilter, OrderingFilter


class DynamicSearchFilter(SearchFilter):
    """If a viewset doesn't declare search_fields, infer all Char/Text field names."""
    def get_search_fields(self, view, request):  # noqa: D401
        fields = getattr(view, 'search_fields', None)
        if fields:
            return fields
        try:
            model = view.get_queryset().model
        except Exception:  # pragma: no cover
            return []
        dynamic = []
        for f in model._meta.fields:
            if f.get_internal_type() in {'CharField', 'TextField'}:
                dynamic.append(f.name)
        return dynamic[:6]  # cap to avoid overly broad queries


class DynamicOrderingFilter(OrderingFilter):
    """If a viewset doesn't declare ordering_fields, allow ordering by all concrete fields."""
    def get_valid_fields(self, queryset, view, context=None):  # noqa: D401
        fields = getattr(view, 'ordering_fields', None)
        if not fields or fields == '__all__':
            return [(f.name, f.verbose_name) for f in queryset.model._meta.fields]
        return super().get_valid_fields(queryset, view, context)