from django import forms
from django.contrib import admin

from account.models import ExternalUser

from .models import Places, Volunteer, Volunteering, VolunteerCategory
from notifications.models import Notification

# Register your models here.
class VolunteeringForm(forms.ModelForm):
    class Meta:
        model = Volunteering
        fields = '__all__'
        widgets = {
            'days': forms.CheckboxSelectMultiple(),
        }

@admin.register(Volunteering)
class VolunteeringAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'place', 'updated_at', 'created_at')
    list_filter = ('category', 'place')
    search_fields = ('title', 'place', 'category')
    date_hierarchy = 'updated_at'
    ordering = ('-updated_at',)

    list_per_page = 25
    list_display_links = ('title',)

    show_facets = admin.ShowFacets.ALWAYS

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)

        if is_new:
            users = ExternalUser.objects.all().exclude(pk=request.user.pk)
            for user in users:
                Notification.objects.create(
                    user=user,
                    volunteering=obj,
                    message=f"Nueva oportunidad de voluntariado: {obj.title}"
                )

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('user', 'volunteering', 'created_at',)
    list_filter = ('volunteering',)
    search_fields = ('user', 'volunteering')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    list_per_page = 25
    list_display_links = ('user',)

    show_facets = admin.ShowFacets.ALWAYS

@admin.register(VolunteerCategory)
class VolunteeringCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'updated_at'
    ordering = ('-updated_at',)
    
    list_per_page = 25
    list_display_links = ('name',)

@admin.register(Places)
class PlacesAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'updated_at'
    ordering = ('-updated_at',)
    
    list_per_page = 25
    list_display_links = ('name',)