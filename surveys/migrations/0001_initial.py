# Generated by Django 5.1.4 on 2025-03-14 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(verbose_name='Pregunta')),
                ('question_type', models.CharField(choices=[('predefinida', 'Predefinida'), ('libre', 'Libre')], max_length=50, verbose_name='Tipo de pregunta')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'verbose_name': 'Pregunta',
                'verbose_name_plural': 'Preguntas',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_text', models.CharField(blank=True, max_length=255, null=True, verbose_name='Opción')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='surveys.question', verbose_name='Pregunta')),
            ],
            options={
                'verbose_name': 'Opción',
                'verbose_name_plural': 'Opciones',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(verbose_name='Respuesta')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.externaluser', verbose_name='Usuario')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.question', verbose_name='Pregunta')),
            ],
            options={
                'verbose_name': 'Respuesta',
                'verbose_name_plural': 'Respuestas',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('start_date', models.DateTimeField(verbose_name='Fecha de inicio')),
                ('end_date', models.DateTimeField(verbose_name='Fecha de finalización')),
                ('status', models.CharField(choices=[('activa', 'Activa'), ('finalizada', 'Finalizada')], default='activa', max_length=60, verbose_name='Estado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('pollster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pollster', to='account.internaluser', verbose_name='Encuestador')),
            ],
            options={
                'verbose_name': 'Encuesta',
                'verbose_name_plural': 'Encuestas',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='surveys.survey', verbose_name='Encuesta'),
        ),
    ]
