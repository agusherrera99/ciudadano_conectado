from django.db import models

# Create your models here.

class Notification(models.Model):
    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ('-created_at',)

    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, verbose_name='Usuario')
    issue = models.ForeignKey('issues.Issue', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Solicitud')
    survey = models.ForeignKey('surveys.Survey', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Encuesta')
    volunteering = models.ForeignKey('volunteering.Volunteering', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Voluntariado')
    message = models.TextField(verbose_name='Mensaje')
    is_read = models.BooleanField(default=False, verbose_name='Leído')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')

    def __str__(self):
        return f"Notificación #{self.id}"