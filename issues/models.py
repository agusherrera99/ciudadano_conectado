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

    PRIORITY_CHOICES = (
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='otro')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    manager = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='manager', blank=True, null=True)
    assigned_to = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='assigned_to', blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='baja')

    def __str__(self):
        return f"Issue: #{self.id}"

class IssueUpdate(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Issue.STATUS_CHOICES, default='pendiente')

    def __str__(self):
        return f"Issue Update: #{self.id} - Issue: #{self.issue.id}"
    