# Generated by Django 4.2.7 on 2023-12-11 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0012_direccioncliente_formapago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccioncliente',
            name='formaPago',
            field=models.CharField(choices=[('contrarrempolso', 'Contrareenbolso'), ('pasarela', 'Tarjeta de crédito')], default='contrarrempolso', max_length=50, verbose_name='Método preferido de pago'),
        ),
    ]