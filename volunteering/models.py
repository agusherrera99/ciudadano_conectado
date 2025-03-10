from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class VolunteerCategory(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Volunteering(models.Model):
    DAYS = (
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miercoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sabado'),
        ('domingo', 'Domingo'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    days = models.CharField(max_length=10, choices=DAYS)
    hours = models.IntegerField()
    place = models.CharField(max_length=100)
    images = models.ImageField(upload_to='volunteering', blank=True, null=True)
    category = models.ForeignKey(VolunteerCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Volunteer(models.Model):
    user = get_user_model()
    volunteering = models.ForeignKey(Volunteering, on_delete=models.CASCADE)