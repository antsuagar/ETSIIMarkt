# Generated by Django 4.2.7 on 2023-11-29 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='direccionenvio',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='cliente',
        ),
        migrations.AddField(
            model_name='direccionenvio',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pedido',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
