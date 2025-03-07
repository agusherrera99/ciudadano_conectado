from django.contrib import admin
from django.contrib.auth import get_user_model
from django.forms import BaseInlineFormSet
from .models import Survey, Question, Option


from notifications.models import Notification

class OptionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Verificar si la pregunta es de tipo "predefinida" y asegurarse de que tenga opciones
        if any(form.cleaned_data and form.cleaned_data.get('DELETE') is False for form in self.forms):
            return
        
        parent_question = self.instance
        if parent_question and parent_question.question_type == 'predefinida':
            raise ValueError("Las preguntas de tipo predefinida deben tener al menos una opción.")

class OptionInline(admin.TabularInline):
    model = Option
    formset = OptionInlineFormSet
    extra = 3
    verbose_name = "Opción"
    verbose_name_plural = "Opciones"

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'created_at', 'updated_at', 'status', 'pollster')
    list_filter = ('updated_at', 'status', 'pollster')
    date_hierarchy = 'updated_at'
    ordering = ('-updated_at', '-status')
    
    list_per_page = 25
    list_display_links = ('name',)
    
    show_facets = admin.ShowFacets.ALWAYS
    
    exclude = ('pollster',)
    
    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None  # Verificar si es una nueva actualización
        if not change:
            obj.pollster = request.user

        super().save_model(request, obj, form, change)
        
        if is_new: 
            users = get_user_model().objects.all().exclude(pk=request.user.pk)
            # Crear notificaciones para los usuarios
            for user in users:
                Notification.objects.create(
                    user=user,
                    survey=obj,
                    message=f"Nueva encuesta: {obj.name}"
                )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_type', 'created_at', 'updated_at', 'survey')
    list_filter = ('question_type', 'survey')
    date_hierarchy = 'updated_at'
    ordering = ('-updated_at',)
    inlines = [OptionInline]
    
    list_per_page = 25
    list_display_links = ('question_text',)
    
    show_facets = admin.ShowFacets.ALWAYS
    
    # Mostrar/ocultar opciones según el tipo de pregunta
    class Media:
        js = ('admin/js/question_admin.js',)
