# Generated by Django 4.2.7 on 2023-12-11 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0008_alter_fabricante_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='icono',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
