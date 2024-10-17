# Generated by Django 5.1.1 on 2024-10-17 09:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point_manager', '0004_player_season_event_participation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='liga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liga', to='point_manager.liga'),
        ),
        migrations.AlterField(
            model_name='event',
            name='managed_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL),
        ),
    ]
