# Generated by Django 5.0.7 on 2024-12-10 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('documento_identidad', models.CharField(max_length=10, unique=True)),
                ('telefono', models.CharField(blank=True, max_length=10, null=True)),
                ('correo_electronico', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('direccion', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
    ]
