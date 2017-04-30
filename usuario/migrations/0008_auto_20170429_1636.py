# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-29 21:36
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0007_auto_20170429_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(error_messages={'required': '\xbfCu\xe1l es el t\xe9lefono?'}, max_length=10, validators=[django.core.validators.RegexValidator(message='El n\xfamero de tel\xe9fono no es v\xe1lido.', regex=b'^([3]([0][0-5]|[1][0-9]|[2][0-2]|[5][01])[0-9]{7})|([2-8][0-9]{6})$')]),
        ),
    ]
