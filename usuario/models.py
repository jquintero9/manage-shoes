#!usr/bin/local
# coding: latin-1

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):

    """
    Modelo Usuario: Representa los usuarios que tendr�n acceso a la
    aplicaci�n, dependiendo del rol (Administrador, Vendedor)
    """

    user = models.OneToOneField(User, primary_key=True)
    nombres = models.CharField(max_length=50)


