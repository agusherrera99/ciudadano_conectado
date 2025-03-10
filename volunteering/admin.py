from django.contrib import admin
from django import forms

from .models import Places, Volunteering, VolunteerCategory

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