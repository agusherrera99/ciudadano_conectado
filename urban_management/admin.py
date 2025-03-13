from django.contrib import admin
from django.db.models import Q

from .models import Ordering, OrderingUpdate
# Register your models here.

@admin.register(Ordering)
class OrderingAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'category', 'status', 'priority', 'created_at', 'manager', 'responsible')
    list_filter = ('category', 'status', 'priority', 'manager', 'responsible')
    search_fields = ('uuid', 'description', 'manager__username', 'responsible__username')
    date_hierarchy = 'updated_at'
    ordering = ('-priority', 'created_at')

    list_per_page = 25
    list_display_links = ('uuid',)

    show_facets = admin.ShowFacets.ALWAYS

    fieldsets = (
        (None, {'fields': ('category', 'description', 'status', 'priority', 'manager', 'responsible')}),
        ('Ubicación', {'fields': ('latitude', 'longitude', 'address')}),
    )

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.manager == request.user or obj.responsible == request.user

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        if obj and (obj.manager == request.user or obj.responsible == request.user):
            return []
        return '__all__'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(manager=request.user) |
            Q(responsible=request.user)
        )
    
@admin.register(OrderingUpdate)
class OrderingUpdateAdmin(admin.ModelAdmin):
    list_display = ('ordering', 'description', 'status', 'updated_at')
    list_filter = ('status',)
    search_fields = ('description', 'ordering__uuid')
    date_hierarchy = 'updated_at'

    list_per_page = 25
    list_display_links = ('ordering',)

    show_facets = admin.ShowFacets.ALWAYS

    fieldsets = (
        (None, {'fields': ('ordering', 'description', 'status')}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'ordering':
            if request.user.is_superuser:
                pass
            else:
                # Managers ven sus ordenamientos, responsables ven los que tienen asignados
                kwargs['queryset'] = Ordering.objects.filter(
                    Q(manager=request.user) | 
                    Q(assigned_to=request.user)
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        if obj and (obj.ordering.manager == request.user or obj.ordering.responsible == request.user):
            return []
        return '__all__'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(ordering__manager=request.user) |
            Q(ordering__responsible=request.user)
        )