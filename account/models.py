from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    is_internal = models.BooleanField(default=False, verbose_name='Usuario interno')
    is_external = models.BooleanField(default=True, verbose_name='Usuario externo')

    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Dirección')
    dni = models.CharField(max_length=20, blank=True, null=True, verbose_name='DNI')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='Fecha de actualización')
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='customuser_permission_set',
        blank=True
    )

    @property
    def specific_instance(self):
        """
        Retorna la instancia específica del usuario.
        (InternalUser o ExternalUser)
        """
        if self.is_internal:
            return self.internaluser
        elif self.is_external:
            return self.externaluser
        else:
            return None

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

# Internos
class Department(models.Model):
    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
    
    name = models.CharField(max_length=255, unique=True, verbose_name='Nombre')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='Fecha de actualización')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.name is not None:
            self.name = self.name.lower()
        
        if self.created_at is None:
            self.created_at = timezone.now()
        
        if self.updated_at is None:
            self.updated_at = timezone.now()

        return super(Department, self).save(*args, **kwargs)
    
class Position(models.Model):
    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
    
    name = models.CharField(max_length=255, unique=True, verbose_name='Nombre')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='Fecha de actualización')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.name is not None:
            self.name = self.name.lower()
        
        if self.created_at is None:
            self.created_at = timezone.now()
        
        if self.updated_at is None:
            self.updated_at = timezone.now()

        return super(Position, self).save(*args, **kwargs)
    
class InternalUser(CustomUser):
    class Meta:
        verbose_name = 'Usuario interno'
        verbose_name_plural = 'Usuarios internos'
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True, related_name='users', verbose_name='Departamento')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True, related_name='users', verbose_name='Cargo')
    
    def __str__(self):
        return f"{self.username} ({self.department.name} - {self.position.name})"
    
    def save(self, *args, **kwargs):
        self.is_internal = True
        self.is_staff = True

        if self.department is not None:
            self.department.name = self.department.name.lower()
        else:
            self.department = Department.objects.get_or_create(name='sin departamento')[0]
        
        if self.position is not None:
            self.position.name = self.position.name.lower()
        else:
            self.position = Position.objects.get_or_create(name='sin cargo')[0]
        
        return super(InternalUser, self).save(*args, **kwargs)

class ExternalUser(CustomUser):
    class Meta:
        verbose_name = 'Usuario externo'
        verbose_name_plural = 'Usuarios externos'
    
    def save(self, *args, **kwargs):
        self.is_external = True
        self.is_internal = False
        self.is_staff = False
        
        return super(ExternalUser, self).save(*args, **kwargs)