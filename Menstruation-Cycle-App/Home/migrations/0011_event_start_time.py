# Generated by Django 3.0.5 on 2023-01-07 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0010_auto_20230107_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(default='2022-05-05'),
            preserve_default=False,
        ),
    ]