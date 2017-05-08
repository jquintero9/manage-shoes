#!usr/local/bin
# coding: latin-1

from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse_lazy
from usuario.utils import regex, error_messages
from usuario.models import Cliente, Usuario


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
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre

    @staticmethod
    def get_choices():
        marcas = Marca.objects.all()
        choices = [('', 'Selecciona una marca')]

        for marca in marcas:
            choices.append((marca.id, marca.nombre))

        return choices


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
        ('deportivo', 'Deportivo'),
        ('formal', 'Formal'),
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
        },
        choices=GENERO
    )

    estilo = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(regex=regex['estilo'], message=error_messages['estilo'])
        ],
        error_messages={
            'required': u'¿Cúal es el estilo?'
        },
        choices=ESTILO
    )

    talla = models.CharField(
        max_length=2,
        validators=[
            RegexValidator(regex=regex['talla'], message=error_messages['talla'])
        ],
        choices=TALLA
    )

    stock = models.PositiveSmallIntegerField(
        validators=[
            RegexValidator(regex=regex['numero'], message=error_messages['numero'])
        ],
        error_messages={
            'required': u'¿Cuantos hay en el inventario?'
        }
    )

    precio = models.PositiveIntegerField(
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

    def get_absolute_url_update(self):
        return reverse_lazy('usuario:actualizar_producto', kwargs={'pk': self.id})

    def get_absolute_url_delete(self):
        return reverse_lazy('usuario:eliminar_producto', kwargs={'pk': self.id})

    def nombre_factura(self):
        return '(%s) %s' % (self.marca.nombre, self.nombre)


class Factura(models.Model):

    """
    Representa el modelo de factura.
    """

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    vendedor = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)

    total_pagar = models.PositiveIntegerField(
        validators=[
            RegexValidator(regex=regex['numero'], message=error_messages['numero'])
        ],
        blank=True,
        default=0
    )

    class Meta:
        db_table = 'facturas'
        verbose_name = 'factura'
        verbose_name_plural = 'facturas'
        ordering = ['-fecha']

    def __unicode__(self):
        return '%s ' % self.id


class DetalleFactura(models.Model):

    """
    Representa el detalle de cada factura.
    """

    factura = models.ForeignKey('Factura', on_delete=models.PROTECT)
    producto = models.ForeignKey('Producto', on_delete=models.PROTECT)

    cantidad = models.PositiveSmallIntegerField(
        validators=[
            RegexValidator(regex=regex['numero'], message=error_messages['numero'])
        ],
        error_messages={
            'required': u'¿Cuantos productos se van a comprar?'
        }
    )

    total = models.PositiveIntegerField(
        validators=[
            RegexValidator(regex=regex['numero'], message=error_messages['numero'])
        ],
        error_messages={
            'required': u'¿Cuál es el valor del producto(s)?'
        },
        blank=True,
        default=0
    )

    class Meta:
        db_table = 'detalle_facturas'
        verbose_name = 'detalle'
        verbose_name_plural = 'detalles'
        unique_together = (('factura', 'producto'),)

    def __unicode__(self):
        return self.producto.nombre




