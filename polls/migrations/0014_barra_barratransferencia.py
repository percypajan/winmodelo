# Generated by Django 3.0.5 on 2020-04-27 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20200427_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='barra',
            name='barratransferencia',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.BarraTransferencia'),
            preserve_default=False,
        ),
    ]
