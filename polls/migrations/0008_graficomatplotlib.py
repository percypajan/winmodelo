# Generated by Django 3.0.5 on 2020-04-27 01:47

from django.db import migrations, models
import django_matplotlib.fields


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_modelo_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraficoMatplotlib',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fig', django_matplotlib.fields.MatplotlibFigureField()),
            ],
        ),
    ]
