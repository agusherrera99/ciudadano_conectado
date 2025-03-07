# Generated by Django 5.1.4 on 2025-03-07 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0009_alter_issue_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
