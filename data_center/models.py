from django.db import models

# Create your models here.
class Areas(models.Model):
    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'

    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')
    api_url = models.URLField(max_length=255, verbose_name='URL API')
    development = models.BooleanField(default=False, verbose_name='En desarrollo')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
