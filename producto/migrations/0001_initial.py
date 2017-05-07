# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-07 05:20
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveSmallIntegerField(error_messages={'required': '\xbfCuantos productos se van a comprar?'}, validators=[django.core.validators.RegexValidator(message='Ingrese solo n\xfameros.', regex=b'^[0-9]+$')])),
                ('total', models.PositiveIntegerField(blank=True, default=0, error_messages={'required': '\xbfCu\xe1l es el valor del producto(s)?'}, validators=[django.core.validators.RegexValidator(message='Ingrese solo n\xfameros.', regex=b'^[0-9]+$')])),
            ],
            options={
                'db_table': 'detalle_facturas',
                'verbose_name': 'detalle',
                'verbose_name_plural': 'detalles',
            },
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total_pagar', models.PositiveIntegerField(blank=True, default=0, validators=[django.core.validators.RegexValidator(message='Ingrese solo n\xfameros.', regex=b'^[0-9]+$')])),
            ],
            options={
                'ordering': ['-fecha'],
                'db_table': 'facturas',
                'verbose_name': 'factura',
                'verbose_name_plural': 'facturas',
            },
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(error_messages={'required': '\xbfCu\xe1l es el nombre de la marca?'}, max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message='Ingrese solo letras.', regex=b'^[A-Za-z\xe1\xe9\xed\xf3\xfa\xc1\xc9\xcd\xd3\xda\\s]+$')])),
            ],
            options={
                'ordering': ['nombre'],
                'db_table': 'marcas',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_referencia', models.CharField(error_messages={'required': '\xbfCu\xe1l es el id del producto?'}, max_length=6, unique=True, validators=[django.core.validators.RegexValidator(message='El formato del ID no es v\xe1lido', regex=b'^[A-Za-z0-9]{6}$')])),
                ('nombre', models.CharField(error_messages={'required': '\xbfCu\xe1l es el nombre del producto?s'}, max_length=40, validators=[django.core.validators.RegexValidator(message='Ingrese solo caracteres alfanumericos', regex=b'^[A-Za-z0-9\\s]+$')])),
                ('genero', models.CharField(choices=[('hombre', 'Hombre'), ('mujer', 'Mujer'), ('unisex', 'Unisex')], error_messages={'required': '\xbfCu\xe1l es el g\xe9nero?'}, max_length=6, validators=[django.core.validators.RegexValidator(message='El g\xe9nero no es v\xe1lido.', regex=b'^hombre|mujer|unisex$')])),
                ('estilo', models.CharField(choices=[('deportivo', 'Deportivo'), ('formal', 'Formal')], error_messages={'required': '\xbfCu\xe1l es el estilo?'}, max_length=9, validators=[django.core.validators.RegexValidator(message='El estilo no es v\xe1lido', regex=b'^deportivo|formal$')])),
                ('stock', models.PositiveSmallIntegerField(error_messages={'required': '\xbfCuantos hay en el inventario?'}, validators=[django.core.validators.RegexValidator(message='Ingrese solo n\xfameros.', regex=b'^[0-9]+$')])),
                ('precio', models.PositiveIntegerField(error_messages={'required': 'Cu\xe1l es el precio del producto?'}, validators=[django.core.validators.RegexValidator(message='Ingrese solo n\xfameros.', regex=b'^[0-9]+$')])),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='producto.Marca')),
            ],
            options={
                'ordering': ['nombre'],
                'db_table': 'productos',
                'verbose_name': 'producto',
                'verbose_name_plural': 'productos',
            },
        ),
        migrations.CreateModel(
            name='Talla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(error_messages={'required': '\xbfCu\xe1l es el n\xfamero de talla?'}, max_length=2, unique=True, validators=[django.core.validators.RegexValidator(message='El n\xfamero de tall no es v\xe1lido', regex=b'^2[7-9]|3[0-9]|4[0-3]$')])),
            ],
            options={
                'db_table': 'tallas',
            },
        ),
        migrations.AddField(
            model_name='producto',
            name='tallas',
            field=models.ManyToManyField(db_table='tallas_producto', related_name='talla_producto', to='producto.Talla'),
        ),
    ]
