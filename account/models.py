from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Dirección')
    dni = models.CharField(max_length=20, blank=True, null=True, verbose_name='DNI')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='Fecha de actualización')
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customuser_set',  # Added a unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='customuser_permission_set',  # Added a unique related_name
        blank=True
    )
    is_internal = models.BooleanField(default=False, verbose_name='Usuario interno')

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.address is not None:
            self.address = self.address.lower()

        if self.created_at is None:
            self.created_at = timezone.now()
        
        if self.updated_at is None:
            self.updated_at = timezone.now()

        return super(CustomUser, self).save(*args, **kwargs)
