# Generated by Django 3.0.5 on 2020-05-12 14:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0063_auto_20200512_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='fecha0',
            field=models.DateField(default=datetime.date(2020, 5, 12), verbose_name='fecha actualizado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cliente',
            name='usuario0',
            field=models.CharField(default=datetime.date(2020, 5, 12), max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='generador',
            name='fecha0',
            field=models.DateField(default=datetime.date(2020, 5, 12), verbose_name='fecha actualizado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='generador',
            name='usuario0',
            field=models.CharField(default=datetime.date(2020, 5, 12), max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='periodo',
            name='fecha0',
            field=models.DateField(default=datetime.date(2020, 5, 12), verbose_name='fecha actualizado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='periodo',
            name='usuario0',
            field=models.CharField(default=datetime.date(2020, 5, 12), max_length=200),
            preserve_default=False,
        ),
    ]
