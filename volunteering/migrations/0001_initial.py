# Generated by Django 5.1.4 on 2025-03-10 15:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

from volunteering.script import init_categories, init_days


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Places',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VolunteerCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Volunteering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('hours', models.IntegerField()),
                ('images', models.ImageField(blank=True, null=True, upload_to='volunteering')),
                ('icon', models.CharField(choices=[('fa-leaf', 'Hoja'), ('fa-hands-helping', 'Manos ayudando'), ('fa-book', 'Libro'), ('fa-heart', 'Corazón'), ('fa-tree', 'Árbol'), ('fa-users', 'Usuarios'), ('fa-seedling', 'Planta'), ('fa-utensils', 'Cubiertos'), ('fa-child', 'Niño'), ('fa-paint-brush', 'Pincel'), ('fa-music', 'Música')], default='fa-heart', help_text='Icono de FontAwesome para mostrar en la tarjeta', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteering.volunteercategory')),
                ('days', models.ManyToManyField(to='volunteering.day')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteering.places')),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', models.CharField(blank=True, default='', max_length=100)),
                ('skills', models.TextField(blank=True, null=True)),
                ('motivation', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('volunteering', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteering.volunteering')),
            ],
        ),
        migrations.RunPython(
            init_categories
        ),
        migrations.RunPython(
            init_days
        )
    ]
