# Generated by Django 3.0.5 on 2020-05-02 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0039_auto_20200502_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='dias',
            name='ddmmyyyy',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
