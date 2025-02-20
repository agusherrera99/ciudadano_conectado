from django.contrib import admin
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Notification

# Register your models here.

class NotificationManagerForm(ModelForm):
    class Meta:
        model = Notification
        fields = ('message', 'is_read')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar usuarios que no son staff, ni superusuario
        User = get_user_model()
        self.fields['user'].queryset = User.objects.filter(
            is_staff=False, is_superuser=False
        ).distinct()

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'issue', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'user')
    search_fields = ('user__username',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    list_per_page = 25
    list_display_links = ('id',)

    show_facets = admin.ShowFacets.ALWAYS

    fieldsets = (
        (None, {'fields': ('user', 'issue', 'message', 'is_read')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        # Si el usuario es superusuario, usar form restringido
        if request.user.is_superuser:
            kwargs['form'] = NotificationManagerForm
        return super().get_form(request, obj, **kwargs)