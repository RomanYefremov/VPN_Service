# Generated by Django 4.2.7 on 2023-11-16 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_vpnserver_rename_user_auth_userauth'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_transitions', models.PositiveIntegerField(default=0)),
                ('data_sent', models.PositiveIntegerField(default=0)),
                ('data_received', models.PositiveIntegerField(default=0)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.site')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='VpnServer',
        ),
    ]