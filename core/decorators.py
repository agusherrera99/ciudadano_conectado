from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps

def internal_user_required(view_func):
    """Restringe el acceso solo a usuarios internos."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_internal:
            raise PermissionDenied  # Retorna un error 403 si el usuario no es interno
        return view_func(request, *args, **kwargs)
    return login_required(_wrapped_view)  # Asegura que el usuario esté autenticado

def external_user_required(view_func):
    """Restringe el acceso solo a usuarios externos."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_internal:
            raise PermissionDenied  # Retorna un error 403 si el usuario es interno
        return view_func(request, *args, **kwargs)
    return login_required(_wrapped_view)  # Asegura que el usuario esté autenticado
