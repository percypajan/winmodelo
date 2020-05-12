# Generated by Django 3.0.5 on 2020-05-04 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0043_registro_barra'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reparto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libre', models.BooleanField(default=True)),
                ('tipo', models.IntegerField(choices=[(0, 'Licitación'), (1, 'Bilateral'), (2, 'C.Libres')], default=1)),
                ('fija', models.FloatField(default=0)),
                ('variable', models.FloatField(default=0)),
                ('fijafp', models.FloatField(default=0)),
                ('variablefp', models.FloatField(default=0)),
                ('fijafact', models.FloatField(default=0)),
                ('variablefact', models.FloatField(default=0)),
                ('fijafptact', models.FloatField(default=0)),
                ('variablefpfact', models.FloatField(default=0)),
                ('coincidente', models.FloatField(default=0)),
                ('barra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Barra')),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Contrato')),
                ('generador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Generador')),
                ('mesano', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Periodo')),
            ],
        ),
    ]
