# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-28 13:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0007_producto_talla'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tallaproducto',
            name='producto',
        ),
        migrations.RemoveField(
            model_name='tallaproducto',
            name='talla',
        ),
        migrations.DeleteModel(
            name='TallaProducto',
        ),
    ]
