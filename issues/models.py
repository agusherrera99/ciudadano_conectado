from django.db import models

# Create your models here.

class Issue(models.Model):
    CATEGORY_CHOICES = (
        ('reclamo', 'Reclamo'),
        ('sugerencia', 'Sugerencia'),
        ('consulta', 'Consulta'),
        ('otro', 'Otro'),
    )
    
    STATUS_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('recibido', 'Recibido'),
        ('en proceso', 'En proceso'),
        ('resuelto', 'Resuelto'),
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='otro')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)

class IssueUpdate(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Issue.STATUS_CHOICES, default='pendiente')
    