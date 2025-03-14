from django.contrib import admin
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.db.models import Q

from .models import Issue, IssueUpdate
from notifications.models import Notification

class IssueManagerForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('priority', 'operator')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar usuarios que pertenecen al grupo issue_trackers
        User = get_user_model()
        self.fields['operator'].queryset = User.objects.filter(
            groups__name='issue_trackers'
        ).distinct()


# Register your models here.

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'votes_count', 'priority', 'status', 'category', 'description', 'user', 'manager', 'operator', 'created_at',)
    list_filter = ('priority', 'status', 'category', 'manager', 'operator')
    search_fields = ('user__username', 'manager__username', 'operator__username')
    date_hierarchy = 'updated_at'
    ordering = ('-votes_count', '-priority')

    list_per_page = 25
    list_display_links = ('uuid',)

    show_facets = admin.ShowFacets.ALWAYS

    fieldsets = (
        (None, {'fields': ('category', 'description', 'user')}),
        ('Estado', {'fields': ('status', 'priority')}),
        ('Personal', {'fields': ('manager', 'operator')}),
        ('Ubicación', {'fields': ('latitude', 'longitude', 'address')}),

    )

    def get_form(self, request, obj=None, **kwargs):
        # Manager de la solicitud usa form restringido
        if obj and obj.manager == request.user:
            kwargs['form'] = IssueManagerForm
        return super().get_form(request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        
        # Solo managers pueden editar
        return obj.manager == request.user

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        if obj and obj.manager == request.user:
            # Para el manager, todo es readonly excepto priority y operator
            return [f for f in [f.name for f in self.model._meta.fields] 
                   if f not in ['priority', 'operator']]
        
        # operadores ven todo readonly
        return [f.name for f in self.model._meta.fields]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        # Managers ven sus solicitudes y operadores ven los que tienen asignados
        return qs.filter(
            Q(manager=request.user) | 
            Q(operator=request.user)
        )

@admin.register(IssueUpdate)
class IssueUpdateAdmin(admin.ModelAdmin):
    list_display = ('issue', 'description', 'status', 'updated_at', 'issue__priority', 'issue__operator')
    list_filter = ('status', 'issue__priority')
    search_fields = ('description',)
    date_hierarchy = 'updated_at'
    ordering = ('-updated_at',)

    list_per_page = 25
    list_display_links = ('issue',)

    show_facets = admin.ShowFacets.ALWAYS

    fieldsets = (
        (None, {'fields': ('issue', 'description', 'status',)}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Personalizar el queryset del campo 'issue' según el usuario
        if db_field.name == 'issue':
            if request.user.is_superuser:
                # Superusuarios pueden ver todos los issues
                pass
            else:
                # Managers ven sus solicitudes y operadores ven los que tienen asignados
                kwargs['queryset'] = Issue.objects.filter(
                    Q(manager=request.user) | 
                    Q(operator=request.user)
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(issue__manager=request.user) | 
            Q(issue__operator=request.user)
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        Notification.objects.create(
            user=obj.issue.user,
            issue=obj.issue,
            message=f'Su solicitud #{obj.issue.uuid} ha sido actualizada.'
        )

        # Actualizar el status del issue
        if 'status' in form.changed_data:
            issue = obj.issue
            issue.status = obj.status
            issue.save()