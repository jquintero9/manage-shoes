# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-22 04:42
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(error_messages={'required': '\xbfC\xfaal es el nombre de la Ciudad?'}, max_length=30, validators=[django.core.validators.RegexValidator(message='Ingrese solo letras.', regex=b'^[A-Za-z\xe1\xe9\xed\xf3\xfa\xc1\xc9\xcd\xd3\xda\\s]+$')])),
            ],
            options={
                'ordering': ['nombre'],
                'db_table': 'ciudades',
                'verbose_name': 'ciudad',
                'verbose_name_plural': 'ciudades',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(error_messages={'required': '\xbfC\xfaal es el n\xfamero de c\xe9dula?'}, max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Solo se admiten n\xfameros.', regex=b'^[0-9]+{10,10}$')])),
                ('nombres', models.CharField(error_messages={'required': '\xbfC\xfaal es tu nombre?'}, max_length=50, validators=[django.core.validators.RegexValidator(message='Ingrese solo letras.', regex=b'^[A-Za-z\xe1\xe9\xed\xf3\xfa\xc1\xc9\xcd\xd3\xda\\s]+$')])),
                ('apellidos', models.CharField(error_messages={'required': '\xbfC\xfaal es tu apellido?'}, max_length=50, validators=[django.core.validators.RegexValidator(message='Ingrese solo letras.', regex=b'^[A-Za-z\xe1\xe9\xed\xf3\xfa\xc1\xc9\xcd\xd3\xda\\s]+$')])),
                ('direccion', models.CharField(error_messages={'required': '\xbfD\xf3nde vives?'}, max_length=80, validators=[django.core.validators.RegexValidator(message='El formato de la direcci\xf3n no es v\xe1lido.', regex=b'^[a-zA-Z0-9#\\-\\s]$')])),
                ('telefono', models.CharField(error_messages={'required': '\xbfC\xfaal es el t\xe9lefono?'}, max_length=10, validators=[django.core.validators.RegexValidator(message='El n\xfamero ingresado no es v\xe1lido.', regex=b'([3]([0][0-5]|[1][0-9]|[2][0-2]|[5][01])[\\d]{7})|([2-8][\\d]{6,6})$')])),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='usuario.Ciudad')),
            ],
            options={
                'ordering': ['apellidos'],
                'db_table': 'clientes',
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(error_messages={'required': '\xbfC\xfaal es el nombre del Departamento?'}, max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Ingrese solo letras.', regex=b'^[A-Za-z\xe1\xe9\xed\xf3\xfa\xc1\xc9\xcd\xd3\xda\\s]+$')])),
            ],
            options={
                'ordering': ['nombre'],
                'db_table': 'departamentos',
                'verbose_name': 'departamento',
                'verbose_name_plural': 'departamentos',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nombres', models.CharField(error_messages={'required': '\xbfC\xfaal es tu nombre?'}, max_length=50, validators=[django.core.validators.RegexValidator(message='Ingrese solo letras.', regex=b'^[A-Za-z\xe1\xe9\xed\xf3\xfa\xc1\xc9\xcd\xd3\xda\\s]+$')])),
                ('apellidos', models.CharField(error_messages={'required': '\xbfC\xfaal es tu apellido?'}, max_length=50, validators=[django.core.validators.RegexValidator(message='Ingrese solo letras.', regex=b'^[A-Za-z\xe1\xe9\xed\xf3\xfa\xc1\xc9\xcd\xd3\xda\\s]+$')])),
                ('rol', models.CharField(error_messages={'required': '\xbfC\xfaal es el rol del usuario?'}, max_length=13, validators=[django.core.validators.RegexValidator(message='El rol no es v\xe1lido', regex=b'^(administrador|vendedor)$')])),
            ],
            options={
                'db_table': 'usuarios',
            },
        ),
        migrations.AddField(
            model_name='ciudad',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.Departamento'),
        ),
    ]
