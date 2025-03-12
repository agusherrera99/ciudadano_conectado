from django.db import models

# Create your models here.
class Survey(models.Model):
    class Meta:
        verbose_name = 'Encuesta'
        verbose_name_plural = 'Encuestas'

    STATUS_CHOICES = (
        ('activa', 'Activa'),
        ('finalizada', 'Finalizada'),
    )

    name = models.CharField(max_length=255, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    start_date = models.DateTimeField(verbose_name='Fecha de inicio')
    end_date = models.DateTimeField(verbose_name='Fecha de finalización')
    status = models.CharField(max_length=60, choices=STATUS_CHOICES, default='activa', verbose_name='Estado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    pollster = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='pollster', blank=True, null=True, verbose_name='Encuestador')

    def __str__(self):
        return f"Encuesta #{self.id}"
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower().strip()
        self.description = self.description.lower().strip()
        super().save(*args, **kwargs)
    
class Question(models.Model):
    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

    QUESTION_TYPES = (
        ('predefinida', 'Predefinida'),
        ('libre', 'Libre')
    )

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='Encuesta', related_name='questions')
    question_text = models.TextField(verbose_name='Pregunta')
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES, verbose_name='Tipo de pregunta')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return self.question_text
    
    def save(self, *args, **kwargs):
        self.question_text = self.question_text.lower().strip()
        super().save(*args, **kwargs)

class Option(models.Model):
    class Meta:
        verbose_name = 'Opción'
        verbose_name_plural = 'Opciones'

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options', verbose_name='Pregunta')
    option_text = models.CharField(max_length=255, blank=True, null=True, verbose_name='Opción')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    def __str__(self):
        return self.option_text
        
    def save(self, *args, **kwargs):
        self.option_text = self.option_text.lower().strip()
        super().save(*args, **kwargs)

class Answer(models.Model):
    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'

    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, verbose_name='Usuario')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Pregunta')
    answer_text = models.TextField(verbose_name='Respuesta')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    def __str__(self):
        return f"Respuesta de {self.user} a {self.question}: {self.answer_text}"
    
    def save(self, *args, **kwargs):
        self.answer_text = self.answer_text.lower().strip()
        super().save(*args, **kwargs)