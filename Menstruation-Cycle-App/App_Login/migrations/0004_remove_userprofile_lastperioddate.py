# Generated by Django 3.2.3 on 2023-01-04 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Login', '0003_alter_userprofile_lastperioddate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='lastperioddate',
        ),
    ]