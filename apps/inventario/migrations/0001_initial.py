# Generated by Django 5.0.7 on 2024-12-10 22:20

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientoInventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now, unique=True)),
                ('total_ventas', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total_compras', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('ordenes_compra', models.ManyToManyField(blank=True, to='compras.ordendecompra')),
            ],
        ),
    ]
