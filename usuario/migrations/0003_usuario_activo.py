# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-22 22:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_auto_20170421_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='activo',
            field=models.BooleanField(default=False),
        ),
    ]
