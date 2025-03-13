# Generated by Django 5.1.4 on 2025-03-13 13:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, max_length=8, unique=True)),
                ('category', models.CharField(blank=True, choices=[('escrombros', 'Escombros'), ('ramas', 'Ramas'), ('malezas', 'Malezas'), ('residuos', 'Residuos'), ('vehiculos abandonados', 'Vehículos abandonados'), ('terrenos baldíos', 'Terrenos baldíos'), ('otro', 'Otro')], max_length=60, verbose_name='Categoría')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('status', models.CharField(choices=[('pendiente', 'Pendiente'), ('en proceso', 'En proceso'), ('resuelto', 'Resuelto')], default='pendiente', max_length=60, verbose_name='Estado')),
                ('priority', models.CharField(choices=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta')], default='alta', max_length=60, verbose_name='Prioridad')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Latitud')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Longitud')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Dirección')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordering_manager', to=settings.AUTH_USER_MODEL, verbose_name='Gestor')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsible', to=settings.AUTH_USER_MODEL, verbose_name='Responsable')),
            ],
            options={
                'verbose_name': 'Ordenamiento',
                'verbose_name_plural': 'Ordenamientos',
            },
        ),
        migrations.CreateModel(
            name='OrderingUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('status', models.CharField(choices=[('pendiente', 'Pendiente'), ('en proceso', 'En proceso'), ('resuelto', 'Resuelto')], default='pendiente', max_length=60, verbose_name='Estado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('ordering', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='urban_management.ordering', verbose_name='Ordenamiento')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsible_updates', to=settings.AUTH_USER_MODEL, verbose_name='Responsable')),
            ],
            options={
                'verbose_name': 'Actualización de ordenamiento',
                'verbose_name_plural': 'Actualizaciones de ordenamiento',
            },
        ),
    ]
