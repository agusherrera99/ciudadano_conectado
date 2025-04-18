# Generated by Django 5.1.4 on 2025-03-14 16:43

import django.db.models.deletion

from django.db import migrations, models
from volunteering.script import init_categories, init_days


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Día',
                'verbose_name_plural': 'Días',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Places',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'verbose_name': 'Lugar',
                'verbose_name_plural': 'Lugares',
            },
        ),
        migrations.CreateModel(
            name='VolunteerCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'verbose_name': 'Categoría de voluntariado',
                'verbose_name_plural': 'Categorías de voluntariado',
            },
        ),
        migrations.CreateModel(
            name='Volunteering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('hours', models.IntegerField(verbose_name='Horas')),
                ('images', models.ImageField(blank=True, null=True, upload_to='volunteering', verbose_name='Imágenes')),
                ('icon', models.CharField(choices=[('fa-leaf', 'Hoja'), ('fa-hands-helping', 'Manos ayudando'), ('fa-book', 'Libro'), ('fa-heart', 'Corazón'), ('fa-tree', 'Árbol'), ('fa-users', 'Usuarios'), ('fa-seedling', 'Planta'), ('fa-utensils', 'Cubiertos'), ('fa-child', 'Niño'), ('fa-paint-brush', 'Pincel'), ('fa-music', 'Música')], default='fa-heart', help_text='Icono de FontAwesome para mostrar en la tarjeta', max_length=30, verbose_name='Icono')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteering.volunteercategory', verbose_name='Categoría')),
                ('days', models.ManyToManyField(to='volunteering.day', verbose_name='Días')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteering.places', verbose_name='Lugar')),
            ],
            options={
                'verbose_name': 'Voluntariado',
                'verbose_name_plural': 'Voluntariados',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', models.CharField(blank=True, default='', max_length=100, verbose_name='Disponibilidad')),
                ('skills', models.TextField(blank=True, null=True, verbose_name='Habilidades')),
                ('motivation', models.TextField(blank=True, null=True, verbose_name='Motivación')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.externaluser', verbose_name='Usuario')),
                ('volunteering', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteering.volunteering', verbose_name='Voluntariado')),
            ],
            options={
                'verbose_name': 'Voluntario',
                'verbose_name_plural': 'Voluntarios',
                'ordering': ['id'],
            },
        ),
        migrations.RunPython(
            init_categories
        ),
        migrations.RunPython(
            init_days
        )
    ]
