# Generated by Django 5.1.4 on 2025-03-07 12:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_notification_issue'),
        ('surveys', '0003_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='surveys.survey'),
        ),
    ]
