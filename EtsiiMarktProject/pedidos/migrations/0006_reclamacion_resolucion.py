# Generated by Django 4.2.7 on 2023-12-07 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0005_remove_reclamacion_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='reclamacion',
            name='resolucion',
            field=models.BooleanField(default=False, verbose_name='Esta resuelto: '),
        ),
    ]
