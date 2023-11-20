# Generated by Django 4.2.7 on 2023-11-19 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_site_user_site_user_auth'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='data_received',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='site',
            name='data_sent',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='site',
            name='transitions_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
