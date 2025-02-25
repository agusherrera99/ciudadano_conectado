from uuid import uuid4

from django.db import models
from django.db.models import F

# Create your models here.

def generate_uuid():
    return uuid4().hex[:8]

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

    uuid = models.CharField(max_length=8, unique=True, default=generate_uuid)
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
        self.description.lower().strip()
        
        if not self.uuid:
            self.uuid = generate_uuid()

        super(Issue, self).save(*args, **kwargs)


class IssueUpdate(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Issue.STATUS_CHOICES, default='pendiente')

    def __str__(self):
        return f"Issue Update: #{self.id} - Issue: #{self.issue.id}"
