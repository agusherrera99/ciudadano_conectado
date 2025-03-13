from django.contrib import admin
from django.db.models import Q
from django.forms import ModelForm

from account.models import InternalUser
from .models import Ordering, OrderingUpdate

class OrderingManagerForm(ModelForm):
    class Meta:
        model = Ordering
        fields = ('priority', 'operator')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar usuarios que pertenecen al grupo ordenamientos_operadores
        internal_user = InternalUser.objects.filter(groups__name='ordenamientos_operadores').distinct()
        self.fields['operator'].queryset = internal_user

@admin.register(Ordering)
class OrderingAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'category', 'status', 'priority', 'created_at', 'manager', 'operator')
    list_filter = ('category', 'status', 'priority', 'manager', 'operator')
    search_fields = ('uuid', 'description', 'manager__username', 'operator__username')
    date_hierarchy = 'updated_at'
    ordering = ('-priority', 'created_at')

    list_per_page = 25
    list_display_links = ('uuid',)

    show_facets = admin.ShowFacets.ALWAYS

    fieldsets = (
        (None, {'fields': ('category', 'description', 'status', 'priority', 'manager', 'operator')}),
        ('Ubicación', {'fields': ('latitude', 'longitude', 'address')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        if obj and obj.manager.id == request.user.id:
            kwargs['form'] = OrderingManagerForm
        return super().get_form(request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        
        if obj is None:
            return True
        return obj.manager.id == request.user.id or obj.operator.id == request.user.id

    def get_readonly_fields(self, request, obj=None):
        """
        Define campos de solo lectura según el rol del usuario
        """
        if request.user.is_superuser:
            return []
        
        # Si estamos creando un nuevo objeto
        if obj is None:
            return []
        
        # Si el usuario es el manager puede cambiar priority y operator
        if obj.manager.id == request.user.id:
            editable_fields = ['priority', 'operator']
            all_fields = [field.name for field in self.model._meta.fields 
                         if field.name not in ['id', 'uuid', 'created_at', 'updated_at']]
            return [f for f in all_fields if f not in editable_fields]
        
        if obj.operator and obj.operator.id == request.user.id:
            return [f for f in [field.name for field in self.model._meta.fields]]
        
        # Para otros usuarios, todo es readonly
        return [field.name for field in self.model._meta.fields]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        # Filtrar para mostrar solo los ordenamientos donde el usuario es manager u operador
        return qs.filter(
            Q(manager=request.user) |
            Q(operator=request.user)
        )

    def save_model(self, request, obj, form, change):
        if not change and not obj.inspector:
            obj.inspector = request.user
            
        super().save_model(request, obj, form, change)
        
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
        (None, {'fields': ('ordering', 'description', 'status',)}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'ordering':
            if not request.user.is_superuser:
                # Mostrar ordenamientos donde el usuario es manager u operador
                kwargs['queryset'] = Ordering.objects.filter(
                    Q(manager=request.user) | 
                    Q(operator=request.user)
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        """
        Define campos de solo lectura según el rol del usuario
        """
        if request.user.is_superuser:
            return []
        
        # Si estamos creando un nuevo objeto
        if obj is None:
            return []
        
        # Para otros usuarios, todo es readonly
        return [field.name for field in self.model._meta.fields]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        # Filtrar actualizaciones de ordenamientos donde el usuario es manager u operador
        return qs.filter(
            Q(ordering__manager=request.user) |
            Q(ordering__operator=request.user)
        )