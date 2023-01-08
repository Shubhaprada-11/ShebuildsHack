# Generated by Django 3.0.5 on 2023-01-07 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0009_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='event',
            name='title',
        ),
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(default='I am happy', max_length=500),
            preserve_default=False,
        ),
    ]