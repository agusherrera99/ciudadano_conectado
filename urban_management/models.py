from django.db import models

class Ordering(models.Model):
    class Meta:
        verbose_name = 'Ordenamiento'
        verbose_name_plural = 'Ordenamientos'

    CATEGORY_CHOICES = (
        ('escombros', 'Escombros'),
        ('ramas', 'Ramas'),
        ('malezas', 'Malezas'),
        ('residuos', 'Residuos'),
        ('vehiculos abandonados', 'Vehículos abandonados'),
        ('terrenos baldios', 'Terrenos baldios'),
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
    
    managers = models.ManyToManyField(
        'account.InternalUser', 
        through='OrderingManager',
        related_name='managed_orders',
        verbose_name='Gestores'
    )
    
    inspector = models.ForeignKey('account.InternalUser', on_delete=models.CASCADE, related_name='order_inspector', blank=True, null=True, verbose_name='inspector')
    operator = models.ForeignKey('account.InternalUser', on_delete=models.CASCADE, related_name='order_operator', blank=True, null=True, verbose_name='Operador')

    photo = models.ImageField(upload_to="ordenamientos/", blank=True, null=True, verbose_name="Foto")

    latitude = models.FloatField(null=True, blank=True, verbose_name='Latitud')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Longitud')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Dirección')

    @property
    def manager(self):
        return self.managers.first()

    def __str__(self):
        return f"Ordenamiento #{self.uuid}"
    
    def save(self, *args, **kwargs):
        self.description = self.description.lower().strip()

        # Generar UUID si no existe
        if not self.uuid:
            if self.category == 'escombros':
                self.uuid = 'ESC' + str(Ordering.objects.filter(category='escombros').count() + 1)
            elif self.category == 'ramas':
                self.uuid = 'RAM' + str(Ordering.objects.filter(category='ramas').count() + 1)
            elif self.category == 'malezas':
                self.uuid = 'MAL' + str(Ordering.objects.filter(category='malezas').count() + 1)
            elif self.category == 'residuos':
                self.uuid = 'RES' + str(Ordering.objects.filter(category='residuos').count() + 1)
            elif self.category == 'vehiculos abandonados':
                self.uuid = 'VAB' + str(Ordering.objects.filter(category='vehiculos abandonados').count() + 1)
            elif self.category == 'terrenos baldios':
                self.uuid = 'TER' + str(Ordering.objects.filter(category='terrenos baldios').count() + 1)
            else:
                self.uuid = 'OTR' + str(Ordering.objects.filter(category='otro').count() + 1)

        # Guardar el objeto
        super(Ordering, self).save(*args, **kwargs)

class OrderingManager(models.Model):
    ordering = models.ForeignKey(Ordering, on_delete=models.CASCADE, related_name='manager_relations')
    manager = models.ForeignKey('account.InternalUser', on_delete=models.CASCADE, related_name='order_relations')
    
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('ordering', 'manager')
        verbose_name = 'Gestor de ordenamiento'
        verbose_name_plural = 'Gestores de ordenamientos'

class OrderingUpdate(models.Model):
    class Meta:
        verbose_name = 'Actualización de ordenamiento'
        verbose_name_plural = 'Actualizaciones de ordenamiento'

    ordering = models.ForeignKey(Ordering, on_delete=models.CASCADE, related_name='updates', verbose_name='Ordenamiento')
    description = models.TextField(verbose_name='Descripción')
    status = models.CharField(max_length=60, choices=Ordering.STATUS_CHOICES, default='pendiente', verbose_name='Estado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return f"Actualización de ordenamiento #{self.id}"
    
    def save(self, *args, **kwargs):
        self.description = self.description.lower().strip()
        super(OrderingUpdate, self).save(*args, **kwargs)