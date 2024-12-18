# Generated by Django 5.0.7 on 2024-12-10 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('direccion', models.TextField(verbose_name='Dirección')),
                ('telefono', models.CharField(max_length=10, verbose_name='Teléfono')),
                ('correo_electronico', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
            ],
        ),
    ]
