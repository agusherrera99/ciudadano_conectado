# Generated by Django 5.1.4 on 2025-02-19 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='dni',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
