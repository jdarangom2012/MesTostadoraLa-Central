from django import template

register = template.Library()

@register.filter
def has_group(user, group_name: str) -> bool:
    """Return True if the user belongs to a group (case-insensitive)."""
    if not getattr(user, 'is_authenticated', False):
        return False
    try:
        return user.groups.filter(name__iexact=group_name).exists()
    except Exception:
        return False
