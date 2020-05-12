# Generated by Django 3.0.5 on 2020-04-28 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0020_modelo_visualizar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contrato',
            name='tipocontrato',
        ),
        migrations.AddField(
            model_name='contrato',
            name='bilateral',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='contrato',
            name='libre',
            field=models.BooleanField(default=True),
        ),
    ]
