# Generated by Django 3.0.5 on 2020-04-27 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_barra'),
    ]

    operations = [
        migrations.AddField(
            model_name='codigo',
            name='barra',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.Barra'),
            preserve_default=False,
        ),
    ]
