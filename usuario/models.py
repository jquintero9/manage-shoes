#!usr/bin/local
# coding: latin-1

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .utils import regex, error_messages


class Usuario(models.Model):

    """
    Modelo Usuario: Representa los usuarios que tendr�n acceso a la
    aplicaci�n, dependiendo del rol (Administrador, Vendedor)
    """

    """
    Estos son los roles que pueden ser asignados a los usuarios.
    """
    ADMIN = 'administrador'
    VENDEDOR = 'vendedor'

    user = models.OneToOneField(User, primary_key=True)

    nombres = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(regex=regex['texto'], message=error_messages['texto'])
        ],
        error_messages={'required': u'�C�al es tu nombre?'}
    )

    apellidos = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(regex=regex['texto'], message=error_messages['texto'])
        ],
        error_messages={'required': u'�C�al es tu apellido?'}
    )

    rol = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(regex=regex['rol'], message=error_messages['rol'])
        ],
        error_messages={'required': u'�C�al es el rol del usuario?'}
    )

    class Meta:
        db_table = 'usuarios'

    def __unicode__(self):
        return self.user.username


class Cliente(models.Model):

    """
    Modelo Cliente: Este modelo representa los clientes que realizan las compras
    en el almac�n.
    """

    cedula = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(regex=regex['cedula'], message=error_messages['cedula'])
        ],
        error_messages={'required': u'�C�al es el n�mero de c�dula?'},
        unique=True
    )

    nombres = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(regex=regex['texto'], message=error_messages['texto'])
        ],
        error_messages={'required': u'�C�al es tu nombre?'}
    )

    apellidos = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(regex=regex['texto'], message=error_messages['texto'])
        ],
        error_messages={'required': u'�C�al es tu apellido?'}
    )

    direccion = models.CharField(
        max_length=80,
        validators=[
            RegexValidator(regex=regex['direccion'], message=error_messages['direccion'])
        ],
        error_messages={'required': u'�D�nde vives?'}
    )

    telefono = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(regex=regex['telefono'], message=error_messages['telefono'])
        ],
        error_messages={'required': u'�C�al es el t�lefono?'}
    )

    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['apellidos']

    def __unicode__(self):
        return '%s - %s %s' % (self.cedula, self.nombres, self.apellidos)

