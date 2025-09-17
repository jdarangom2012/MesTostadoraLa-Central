from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name: str):
    """Return True if the authenticated user belongs to the given group (case-insensitive)."""
    if not getattr(user, 'is_authenticated', False):
        return False
    return user.groups.filter(name__iexact=group_name).exists()
