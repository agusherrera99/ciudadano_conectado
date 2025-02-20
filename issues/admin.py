from django.contrib import admin
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.db.models import Q

from .models import Issue, IssueUpdate

class IssueManagerForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('priority', 'assigned_to')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar usuarios que pertenecen al grupo issue_trackers
        User = get_user_model()
        self.fields['assigned_to'].queryset = User.objects.filter(
            groups__name='issue_trackers'
        ).distinct()


# Register your models here.

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'priority', 'status', 'category', 'description', 'user', 'created_at', 'manager', 'assigned_to')
    list_filter = ('priority', 'status', 'category', 'manager', 'assigned_to')
    search_fields = ('user__username', 'manager__username', 'assigned_to__username')
    date_hierarchy = 'updated_at'
    ordering = ('-priority',)

    list_per_page = 25
    list_display_links = ('id',)

    show_facets = admin.ShowFacets.ALWAYS

    fieldsets = (
        (None, {'fields': ('category', 'description', 'user', 'priority', 'status', 'manager', 'assigned_to')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        # Si el usuario es manager del issue, usar form restringido
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
            # Para el manager, todo es readonly excepto priority y assigned_to
            return [f for f in [f.name for f in self.model._meta.fields] 
                   if f not in ['priority', 'assigned_to']]
        # Issue trackers ven todo readonly
        return [f.name for f in self.model._meta.fields]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Managers ven sus issues, trackers ven los que tienen asignados
        return qs.filter(
            Q(manager=request.user) | 
            Q(assigned_to=request.user)
        )

@admin.register(IssueUpdate)
class IssueUpdateAdmin(admin.ModelAdmin):
    list_display = ('issue', 'description', 'status', 'updated_at', 'issue__priority', 'issue__assigned_to')
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(issue__manager=request.user) | 
            Q(issue__assigned_to=request.user)
        )