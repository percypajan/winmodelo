# Generated by Django 3.0.5 on 2020-04-27 23:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20200427_1828'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barra',
            name='barratransferencias',
        ),
    ]
