# Generated by Django 3.0.5 on 2020-05-12 17:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0066_auto_20200512_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='fecha0',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='barra',
            name='fecha0',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='fecha0',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='codigo',
            name='fecha0',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='fecha0',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='contratomes',
            name='fecha0',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='generador',
            name='fecha0',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='registro',
            name='fecha0',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='reparto',
            name='fecha0',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
    ]
