from django.db import models


# Create your models here.
class Day(models.Model):
    class Meta:
        verbose_name = 'Día'
        verbose_name_plural = 'Días'
        ordering = ['id']

    name = models.CharField(max_length=20, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name


class Places(models.Model):
    class Meta:
        verbose_name = "Lugar"
        verbose_name_plural = "Lugares"

    name = models.CharField(max_length=100, verbose_name='Nombre')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return self.name


class VolunteerCategory(models.Model):
    class Meta:
        verbose_name = "Categoría de voluntariado"
        verbose_name_plural = "Categorías de voluntariado"

    name = models.CharField(max_length=100, verbose_name='Nombre')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return self.name
    

class Volunteering(models.Model):
    class Meta:
        verbose_name = 'Voluntariado'
        verbose_name_plural = 'Voluntariados'
        ordering = ['id']

    ICON_CHOICES = [
        ('fa-leaf', 'Hoja'),
        ('fa-hands-helping', 'Manos ayudando'),
        ('fa-book', 'Libro'),
        ('fa-heart', 'Corazón'),
        ('fa-tree', 'Árbol'),
        ('fa-users', 'Usuarios'),
        ('fa-seedling', 'Planta'),
        ('fa-utensils', 'Cubiertos'),
        ('fa-child', 'Niño'),
        ('fa-paint-brush', 'Pincel'),
        ('fa-music', 'Música'),
    ]

    title = models.CharField(max_length=100, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    
    days = models.ManyToManyField(Day, verbose_name='Días')
    hours = models.IntegerField(verbose_name='Horas')
    
    place = models.ForeignKey(Places, on_delete=models.CASCADE, verbose_name='Lugar')
    images = models.ImageField(upload_to="volunteering", blank=True, null=True, verbose_name='Imágenes')
    
    category = models.ForeignKey(VolunteerCategory, on_delete=models.CASCADE, verbose_name='Categoría')
    icon = models.CharField(
        max_length=30, 
        choices=ICON_CHOICES, 
        default='fa-heart', 
        verbose_name='Icono',
        help_text='Icono de FontAwesome para mostrar en la tarjeta'
    
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return self.title
    
    def get_days_display(self):
        """
        Muestra los días en formato legible:
        - Días consecutivos como rango (ej: "Lunes a Jueves")
        - Días no consecutivos separados por comas (ej: "Lunes, Miércoles, Viernes")
        - Un solo día tal cual (ej: "Sábados")
        """
        days = list(self.days.all().order_by('id'))
        
        # Si no hay días o solo hay uno
        if not days:
            return "No especificado"
        elif len(days) == 1:
            return days[0].name
        
        # Comprobamos si son días consecutivos
        consecutive = True
        day_ids = [day.id for day in days]
        
        # Verificar si los IDs son consecutivos
        for i in range(len(day_ids) - 1):
            if day_ids[i + 1] - day_ids[i] != 1:
                consecutive = False
                break
                
        if consecutive:
            # Si son consecutivos, mostrar rango
            return f"{days[0].name} a {days[-1].name}"
        else:
            # Si no son consecutivos, mostrar separados por coma
            return ", ".join([day.name for day in days])
        
    def save(self, *args, **kwargs):
        # Eliminar espacios al principio y al final
        self.title = self.title.strip()
        self.description = self.description.strip()
        
        super(Volunteering, self).save(*args, **kwargs)


class Volunteer(models.Model):
    class Meta:
        verbose_name = 'Voluntario'
        verbose_name_plural = 'Voluntarios'
        ordering = ['id']

    user = models.ForeignKey('account.ExternalUser', on_delete=models.CASCADE, verbose_name='Usuario')
    volunteering = models.ForeignKey(Volunteering, on_delete=models.CASCADE, verbose_name='Voluntariado')
    availability = models.CharField(max_length=100, blank=True, default='', verbose_name='Disponibilidad')
    skills = models.TextField(blank=True, null=True, verbose_name='Habilidades')
    motivation = models.TextField(blank=True, null=True, verbose_name='Motivación')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __str__(self):
        return f"{self.user.username} - {self.volunteering.title}"
    
    def save(self, *args, **kwargs):
        # Eliminar espacios al principio y al final
        self.skills = self.skills.strip()
        self.motivation = self.motivation.strip()

        # Asegurar que availability sea una cadena separada por comas
        if self.availability:
            self.availability = ",".join(self.availability.split(","))
        else:
            self.availability = ""
        
        super(Volunteer, self).save(*args, **kwargs)
