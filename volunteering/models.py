from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Day(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']


class Places(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class VolunteerCategory(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Volunteering(models.Model):
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

    title = models.CharField(max_length=100)
    description = models.TextField()
    days = models.ManyToManyField(Day)
    hours = models.IntegerField()
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="volunteering", blank=True, null=True)
    category = models.ForeignKey(VolunteerCategory, on_delete=models.CASCADE)
    icon = models.CharField(
        max_length=30, 
        choices=ICON_CHOICES, 
        default='fa-heart', 
        help_text='Icono de FontAwesome para mostrar en la tarjeta'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


class Volunteer(models.Model):
    user = get_user_model()
    volunteering = models.ForeignKey(Volunteering, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.volunteering.title}"
