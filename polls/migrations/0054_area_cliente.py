# Generated by Django 3.0.5 on 2020-05-11 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0053_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='cliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.Cliente'),
            preserve_default=False,
        ),
    ]
