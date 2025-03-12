from django.db import models
from django.db.models import F

# Create your models here.
class Issue(models.Model):
    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'

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

    uuid = models.CharField(max_length=8, unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='otro', verbose_name='Categoría')
    description = models.TextField(verbose_name='Descripción')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    votes = models.ManyToManyField('account.CustomUser', related_name='votes', blank=True, verbose_name='Votos')
    votes_count = models.IntegerField(default=0, verbose_name='Cantidad de votos')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente', verbose_name='Estado')
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='user', verbose_name='Usuario')
    manager = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='manager', blank=True, null=True, verbose_name='Responsable')
    assigned_to = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='assigned_to', blank=True, null=True, verbose_name='Asignado a')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='baja', verbose_name='Prioridad')

    # Campos para coordenadas geográficas
    latitude = models.FloatField(null=True, blank=True, verbose_name='Latitud')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Longitud')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Dirección')

    def add_vote(self, user):
        if user not in self.votes.all():
            self.votes.add(user)
            self.votes_count = F('votes_count') + 1 
            self.save(update_fields=['votes_count'])

    def remove_vote(self, user):
        if user in self.votes.all():
            self.votes.remove(user)
            self.votes_count = F('votes_count') - 1 
            self.save(update_fields=['votes_count'])

    def __str__(self):
        return f"Issue: #{self.uuid}"
    
    def save(self, *args, **kwargs):
        self.description = self.description.lower().strip()
        
        if not self.uuid:
            if self.category == 'reclamo':
                self.uuid = f"R-{Issue.objects.filter(category='reclamo').count() + 1}"
            elif self.category == 'sugerencia':
                self.uuid = f"S-{Issue.objects.filter(category='sugerencia').count() + 1}"
            elif self.category == 'consulta':
                self.uuid = f"C-{Issue.objects.filter(category='consulta').count() + 1}"
            else:
                self.uuid = f"O-{Issue.objects.filter(category='otro').count() + 1}"

        super(Issue, self).save(*args, **kwargs)


class IssueUpdate(models.Model):
    class Meta:
        verbose_name = 'Actualización de solicitud'
        verbose_name_plural = 'Actualizaciones de solicitudes'

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Issue.STATUS_CHOICES, default='pendiente')

    def __str__(self):
        return f"Issue Update: #{self.id} - Issue: {self.issue.uuid}"
    
    def save(self, *args, **kwargs):
        self.description = self.description.lower().strip()
        super(IssueUpdate, self).save(*args, **kwargs)
