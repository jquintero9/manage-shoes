#!usr/local/bin
# coding: latin-1

from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
from usuario.utils import regex, error_messages


class Marca(models.Model):

    """
    Representa la marca de los zapatos.
    """

    nombre = models.CharField(
        max_length=30,
        unique=True,
        validators=[
            RegexValidator(regex=regex['texto'], message=error_messages['texto'])
        ],
        error_messages={
            'required': u'¿Cuál es el nombre de la marca?'
        }
    )

    class Meta:
        db_table = 'marcas'
        verbose_name = 'marca'
        verbose_name_plural = 'marcas'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre


class Producto(models.Model):

    """
    Representa los productos que vende la empresa.
    """

    GENERO = (
        ('hombre', 'Hombre'),
        ('mujer', 'Mujer'),
        ('unisex', 'Unisex'),
    )

    ESTILO = (
        ('deportivo', 'deportivo'),
        ('formal', 'formal'),
    )

    TALLA = (
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('32', '32'),
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
    )

    id_referencia = models.CharField(
        max_length=6,
        unique=True,
        validators=[
            RegexValidator(regex=regex['id_referencia'], message=error_messages['id_referencia'])
        ],
        error_messages={
            'required': u'¿Cuál es el id del producto?'
        }
    )

    marca = models.ForeignKey('Marca', on_delete=models.PROTECT)

    nombre = models.CharField(
        max_length=40,
        validators=[
            RegexValidator(regex=regex['nombre_producto'], message=error_messages['nombre_producto'])
        ],
        error_messages={
            'required': u'¿Cuál es el nombre del producto?s'
        }
    )

    genero = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(regex=regex['genero'], message=error_messages['genero'])
        ],
        error_messages={
            'required': u'¿Cuál es el género?'
        }
    )

    estilo = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(regex=regex['estilo'], message=error_messages['estilo'])
        ],
        error_messages={
            'required': u'¿Cuál es el estilo?'
        }
    )

    talla = models.CharField(
        max_length=2,
        validators=[
            RegexValidator(regex=regex['talla'], message=error_messages['talla'])
        ],
        error_messages={
            'required': u'¿Cuál es la talla?'
        }
    )

    stock = models.PositiveSmallIntegerField(
        validators=[
            RegexValidator(regex=regex['numero'], message=error_messages['numero'])
        ],
        error_messages={
            'required': u'¿Cuantos hay en el inventario?'
        }
    )

    precio = models.IntegerField(
        validators=[
            RegexValidator(regex=regex['numero'], message=error_messages['numero'])
        ],
        error_messages={
            'required': u'Cuál es el precio del producto?'
        }
    )

    class Meta:
        db_table = 'productos'
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre


