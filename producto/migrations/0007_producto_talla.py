# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-28 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0006_auto_20170428_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='talla',
            field=models.ManyToManyField(db_table='tallas_producto', related_name='talla_producto', to='producto.Talla'),
        ),
    ]