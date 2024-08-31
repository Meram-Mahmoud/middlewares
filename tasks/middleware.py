from .models import ActivityLog
from django.utils.deprecation import MiddlewareMixin

class ActivityLoggingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            ActivityLog.objects.create(
                user=request.user,
                endpoint=request.path,
                method=request.method
            )
