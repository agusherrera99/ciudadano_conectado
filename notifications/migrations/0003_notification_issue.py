# Generated by Django 5.1.4 on 2025-02-20 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0006_remove_issueupdate_created_at_issueupdate_updated_at'),
        ('notifications', '0002_rename_read_notification_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='issue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='issues.issue'),
        ),
    ]
