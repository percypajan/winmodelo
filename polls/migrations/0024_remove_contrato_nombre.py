# Generated by Django 3.0.5 on 2020-04-30 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0023_contrato_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contrato',
            name='nombre',
        ),
    ]
