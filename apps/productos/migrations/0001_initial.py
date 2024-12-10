# Generated by Django 5.0.7 on 2024-12-10 22:20

import django.db.models.deletion
import simple_history.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_categoria', models.CharField(choices=[('alimentos', 'Alimentos'), ('belleza', 'Belleza'), ('deportes', 'Deportes'), ('electrodomesticos', 'Electrodomésticos'), ('higiene_y_salud', 'Higiene y Salud'), ('maquillaje', 'Maquillaje'), ('vestuario', 'Vestuario'), ('tecnologia', 'Tecnología'), ('jugueteria', 'Juguetería'), ('papeleria', 'Papelería'), ('musica_y_cine', 'Música y Cine'), ('mascotas', 'Mascotas'), ('televisores', 'Televisores'), ('computadores', 'Computadores')], max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('cantidad_en_stock', models.PositiveIntegerField(default=0)),
            ],
            options={
                'permissions': [('view_dashboard', 'Puede ver el dashboard')],
            },
        ),
        migrations.CreateModel(
            name='HistoricalProducto',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('cantidad_en_stock', models.PositiveIntegerField(default=0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('categoria', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='productos.categoria')),
            ],
            options={
                'verbose_name': 'historical producto',
                'verbose_name_plural': 'historical productos',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]