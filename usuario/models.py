#!usr/bin/local
# coding: latin-1

from __future__ import unicode_literals

from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .utils import regex, error_messages


class Usuario(models.Model):

    """
    Modelo Usuario: Representa los usuarios que tendrán acceso a la
    aplicación, dependiendo del rol (Administrador, Vendedor)
    """

    """
    Estos son los roles que pueden ser asignados a los usuarios.
    """
    ADMIN = 'administrador'
    VENDEDOR = 'vendedor'

    PERMISO_ADMIN = 'usuario.es_administrador'
    PERMISO_VENDEDOR = 'usuario.es_vendedor'

    user = models.OneToOneField(User, primary_key=True)

    nombres = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(regex=regex['texto'], message=error_messages['texto'])
        ],
        error_messages={'required': u'¿Cuál es tu nombre?'}
    )

    apellidos = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(regex=regex['texto'], message=error_messages['texto'])
        ],
        error_messages={'required': u'¿Cuál es tu apellido?'}
    )

    rol = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(regex=regex['rol'], message=error_messages['rol'])
        ],
        error_messages={'required': u'¿Cuál es el rol del usuario?'},
        choices=((ADMIN, 'Administrador'), (VENDEDOR, 'Vendedor'))
    )

    activo = models.BooleanField(default=False)

    class Meta:
        db_table = 'usuarios'
        permissions = [
            ('es_administrador', 'es administrador'),
            ('es_vendedor', 'es vendedor')
        ]

    def nombre_completo(self):
        return '%s %s' % (self.nombres, self.apellidos)

    def __unicode__(self):
        return self.user.username


class Departamento(models.Model):

    """
    Modelo Departamento: Representa los departamentos de Colombia.
    """

    nombre = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(regex=regex['texto'], message=error_messages['texto'])
        ],
        error_messages={'required': u'¿Cuál es el nombre del Departamento?'},
        unique=True
    )

    class Meta:
        db_table = 'departamentos'
        verbose_name = 'departamento'
        verbose_name_plural = 'departamentos'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre


class Ciudad(models.Model):

    """
    Modelo Ciudad: Representa las ciudades donde viven los clientes.
    """

    nombre = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(regex=regex['texto'], message=error_messages['texto'])
        ],
        error_messages={'required': u'¿Cuál es el nombre de la Ciudad?'}
    )

    departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE)

    class Meta:
        db_table = 'ciudades'
        verbose_name = 'ciudad'
        verbose_name_plural = 'ciudades'
        ordering = ['nombre']

    def __unicode__(self):
        return '%s (%s)' % (self.nombre, self.departamento)


class Cliente(models.Model):

    """
    Modelo Cliente: Este modelo representa los clientes que realizan las compras
    en el almacén.
    """

    cedula = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(regex=regex['cedula'], message=error_messages['cedula'])
        ],
        error_messages={'required': u'¿Cuál es el número de cédula?'},
        unique=True
    )

    nombres = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(regex=regex['texto'], message=error_messages['texto'])
        ],
        error_messages={'required': u'¿Cuál es tu nombre?'}
    )

    apellidos = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(regex=regex['texto'], message=error_messages['texto'])
        ],
        error_messages={'required': u'¿Cuál es tu apellido?'}
    )

    ciudad = models.ForeignKey('Ciudad', on_delete=models.PROTECT)

    direccion = models.CharField(
        max_length=80,
        validators=[
            RegexValidator(regex=regex['direccion'], message=error_messages['direccion'])
        ],
        error_messages={'required': u'¿Dónde vives?'}
    )

    telefono = models.CharField(
        max_length=10,
        error_messages={'required': u'¿Cuál es el télefono?'}
    )

    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['apellidos']

    def __unicode__(self):
        return '%s - %s %s' % (self.cedula, self.nombres, self.apellidos)

    def nombre_completo(self):
        return '%s %s' % (self.nombres, self.apellidos)

    def get_absolute_url_edit(self):
        return reverse_lazy('usuario:actualizar_cliente', kwargs={'pk': self.id})

    def get_absolute_url_delete(self):
        return reverse_lazy('usuario:eliminar_cliente', kwargs={'pk': self.id})
