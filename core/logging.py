import logging
from .middleware import correlation_id_ctx, current_user_ctx


class CorrelationIdFilter(logging.Filter):
    def filter(self, record):  # noqa: D401
        cid = correlation_id_ctx.get()
        user = current_user_ctx.get()
        record.correlation_id = cid or '-'
        record.user = getattr(user, 'username', '-') if user else '-'
        return True