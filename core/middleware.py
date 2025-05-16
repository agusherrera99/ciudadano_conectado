from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs siempre excluidas del modo mantenimiento (independientemente del usuario)
        self.always_excluded_paths = [
            '/static/',  # Archivos estáticos
            '/media/',   # Archivos multimedia
            '/admin/login/',  # Permite a todos acceder a la página de login
            '/admin/jsi18n/',  # Necesario para el funcionamiento correcto del admin
        ]
        
        # URLs permitidas solo para superusuarios durante mantenimiento
        self.superuser_only_paths = [
            '/admin/',  # Panel de administración solo para superusuarios
        ]
        
    def __call__(self, request):
        try:
            # Importamos aquí para evitar problemas de importación circular
            from systemSetup.models import SystemConfig
            
            # Verificar si el modo mantenimiento está activo
            maintenance_mode = SystemConfig.get_value('MAINTENANCE_MODE', False)
            
            # Si no estamos en modo mantenimiento, continúa normalmente
            if not maintenance_mode:
                return self.get_response(request)
            
            # Comprobar si la URL actual está siempre excluida
            if any(request.path.startswith(path) for path in self.always_excluded_paths):
                return self.get_response(request)
            
            # Verificar si es superusuario (y está autenticado)
            is_superuser = hasattr(request, 'user') and request.user.is_authenticated and request.user.is_superuser
            
            # Si no es superusuario pero está en una ruta de admin
            if not is_superuser and any(request.path.startswith(path) for path in self.superuser_only_paths):
                # Si no está autenticado, redirigir a login
                if not hasattr(request, 'user') or not request.user.is_authenticated:
                    login_url = reverse('admin:login')
                    return redirect_to_login(request.path, login_url=login_url)
                
                # Si está autenticado pero no es superusuario (incluyendo staff)
                # mostrar página de mantenimiento
                return self.show_maintenance_page(request)
            
            # Si es superusuario, permitir acceso a cualquier ruta
            if is_superuser:
                return self.get_response(request)
            
            # Para cualquier otro caso (usuario común, staff no superusuario, etc.)
            # mostrar página de mantenimiento
            return self.show_maintenance_page(request)
            
        except Exception as e:
            # En caso de error, registrar y permitir que la solicitud continúe
            import logging
            logger = logging.getLogger('django')
            logger.error(f"Error en MaintenanceModeMiddleware: {str(e)}")
            return self.get_response(request)
    
    def show_maintenance_page(self, request):
        context = {}
        return render(request, 'maintenance.html', context, status=503)