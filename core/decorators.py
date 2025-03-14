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

def position_required(position_name):
    """
    Restringe el acceso a usuarios internos con un cargo específico.
    Requiere que el usuario tenga acceso a su propiedad specific_instance.
    
    Uso:
    @position_required('inspector')
    def mi_vista(request):
        # código de la vista
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Verifica que sea un usuario interno
            if not request.user.is_authenticated or not request.user.is_internal:
                raise PermissionDenied
                
            # Obtiene la instancia específica del usuario
            user = request.user.specific_instance
            
            # Verifica que tenga un cargo y que sea el requerido
            if not hasattr(user, 'position') or not user.position or user.position.name != position_name:
                raise PermissionDenied
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
