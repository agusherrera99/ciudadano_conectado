from django.db import models

# Create your models here.
class Ordering(models.Model):
    class Meta:
        verbose_name = 'Ordenamiento'
        verbose_name_plural = 'Ordenamientos'

    CATEGORY_CHOICES = (
        ('escrombros', 'Escombros'),
        ('ramas', 'Ramas'),
        ('malezas', 'Malezas'),
        ('residuos', 'Residuos'),
        ('vehiculos abandonados', 'Vehículos abandonados'),
        ('terrenos baldíos', 'Terrenos baldíos'),
        ('otro', 'Otro'),
    )

    STATUS_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('en proceso', 'En proceso'),
        ('resuelto', 'Resuelto'),
    )

    PRIORITY_CHOICES = (
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    )

    uuid = models.CharField(max_length=8, unique=True, blank=True)
    category = models.CharField(max_length=60, choices=CATEGORY_CHOICES, blank=True, verbose_name='Categoría')
    description = models.TextField(verbose_name='Descripción')
    status = models.CharField(max_length=60, choices=STATUS_CHOICES, default='pendiente', verbose_name='Estado')
    priority = models.CharField(max_length=60, choices=PRIORITY_CHOICES, default='alta', verbose_name='Prioridad')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    manager = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='ordering_manager', blank=True, null=True, verbose_name='Gestor')
    responsible = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='responsible', blank=True, null=True, verbose_name='Responsable')

    latitude = models.FloatField(null=True, blank=True, verbose_name='Latitud')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Longitud')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Dirección')

    def __str__(self):
        return f"Ordenamiento #{self.uuid}"
    
    def save(self, *args, **kwargs):
        self.description = self.description.lower().strip()

        if not self.uuid:
            if self.category == 'escrombros':
                self.uuid = 'ESC' + str(Ordering.objects.filter(category='escrombros').count() + 1).zfill(4)
            elif self.category == 'ramas':
                self.uuid = 'RAM' + str(Ordering.objects.filter(category='ramas').count() + 1).zfill(4)
            elif self.category == 'malezas':
                self.uuid = 'MAL' + str(Ordering.objects.filter(category='malezas').count() + 1).zfill(4)
            elif self.category == 'residuos':
                self.uuid = 'RES' + str(Ordering.objects.filter(category='residuos').count() + 1).zfill(4)
            elif self.category == 'vehiculos abandonados':
                self.uuid = 'VAB' + str(Ordering.objects.filter(category='vehiculos abandonados').count() + 1).zfill(4)
            elif self.category == 'terrenos baldíos':
                self.uuid = 'TER' + str(Ordering.objects.filter(category='terrenos baldíos').count() + 1).zfill(4)
            else:
                self.uuid = 'OTR' + str(Ordering.objects.filter(category='otro').count() + 1).zfill(4)

        super(Ordering, self).save(*args, **kwargs)

class OrderingUpdate(models.Model):
    class Meta:
        verbose_name = 'Actualización de ordenamiento'
        verbose_name_plural = 'Actualizaciones de ordenamiento'

    ordering = models.ForeignKey(Ordering, on_delete=models.CASCADE, related_name='updates', verbose_name='Ordenamiento')
    description = models.TextField(verbose_name='Descripción')
    status = models.CharField(max_length=60, choices=Ordering.STATUS_CHOICES, default='pendiente', verbose_name='Estado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    responsible = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='responsible_updates', blank=True, null=True, verbose_name='Responsable')

    def __str__(self):
        return f"Actualización de ordenamiento #{self.id}"
    
    def save(self, *args, **kwargs):
        self.description = self.description.lower().strip()
        super(OrderingUpdate, self).save(*args, **kwargs)