import uuid
import contextvars
from django.conf import settings

# Context variables for correlation id and current user
correlation_id_ctx = contextvars.ContextVar('correlation_id', default=None)
current_user_ctx = contextvars.ContextVar('current_user', default=None)


class CorrelationIdMiddleware:
    """Extract or create a correlation id per request."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        header_name = getattr(settings, 'CORRELATION_ID_HEADER', 'HTTP_X_CORRELATION_ID')
        cid = request.META.get(header_name)
        if not cid:
            cid = str(uuid.uuid4())
        correlation_id_ctx.set(cid)
        request.correlation_id = cid
        response = self.get_response(request)
        response['X-Correlation-Id'] = cid
        return response


class CurrentUserMiddleware:
    """Store current authenticated user in context var for logging/audit."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_user_ctx.set(request.user)
        else:
            current_user_ctx.set(None)
        return self.get_response(request)