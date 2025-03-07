from django.db import models
from django.db.models import F

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

    uuid = models.CharField(max_length=8, unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='otro')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.ManyToManyField('account.CustomUser', related_name='votes', blank=True)
    votes_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    manager = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='manager', blank=True, null=True)
    assigned_to = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='assigned_to', blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='baja')

    # Campos para coordenadas geográficas
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)

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
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Issue.STATUS_CHOICES, default='pendiente')

    def __str__(self):
        return f"Issue Update: #{self.id} - Issue: {self.issue.uuid}"
    
    def save(self, *args, **kwargs):
        self.description = self.description.lower().strip()
        super(IssueUpdate, self).save(*args, **kwargs)
