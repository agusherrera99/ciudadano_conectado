from django.contrib import admin
from .models import SystemConfig

@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description')
    search_fields = ('key', 'description')
    
    fieldsets = (
        (None, {
            'fields': ('key', 'value', 'description')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Solo permitir eliminar configuraciones si el usuario es superusuario
        return request.user.is_superuser
