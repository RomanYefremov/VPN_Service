# Generated by Django 4.2.7 on 2023-11-16 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_sitecreationform'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.userauth')),
            ],
        ),
        migrations.RemoveField(
            model_name='site',
            name='user',
        ),
        migrations.DeleteModel(
            name='SiteCreationForm',
        ),
        migrations.AlterField(
            model_name='statistics',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.website'),
        ),
        migrations.DeleteModel(
            name='Site',
        ),
    ]
