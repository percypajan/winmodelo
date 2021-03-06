# Generated by Django 3.0.5 on 2020-05-11 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0056_area_clase'),
    ]

    operations = [
        migrations.AddField(
            model_name='codigo',
            name='modo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='area',
            name='clase',
            field=models.IntegerField(choices=[(0, 'Ninguna'), (1, 'Selección'), (2, 'Todas')], default=1),
        ),
        migrations.AlterField(
            model_name='codigo',
            name='signo',
            field=models.IntegerField(choices=[(1, '+'), (-1, '-')], default=1),
        ),
    ]
