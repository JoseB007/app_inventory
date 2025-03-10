# Generated by Django 5.0.7 on 2024-12-10 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_empresa', models.CharField(help_text='Establecer el nombre de su empresa', max_length=150, verbose_name='Nombre de la empresa')),
                ('nit', models.CharField(max_length=10, verbose_name='NIT')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo electrónico')),
                ('telefono', models.CharField(max_length=10, verbose_name='Télefono')),
            ],
        ),
    ]
