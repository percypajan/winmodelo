# Generated by Django 3.0.5 on 2020-04-30 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0027_auto_20200430_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='fechafin',
            field=models.DateField(default='01-01-2020', verbose_name='Fecha fin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contrato',
            name='fechaini',
            field=models.DateField(default='01-01-2021', verbose_name='Fecha inicio'),
            preserve_default=False,
        ),
    ]
