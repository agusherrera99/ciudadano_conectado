from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    dni = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
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

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        self.address = self.address.lower()

        if self.created_at is None:
            self.created_at = timezone.now()
        
        if self.updated_at is None:
            self.updated_at = timezone.now()

        return super(CustomUser, self).save(*args, **kwargs)
