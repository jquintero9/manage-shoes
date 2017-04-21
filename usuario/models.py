#!usr/bin/local
# coding: latin-1

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):

    """
    Modelo Usuario: Representa los usuarios que tendrán acceso a la
    aplicación, dependiendo del rol (Administrador, Vendedor)
    """

    user = models.OneToOneField(User, primary_key=True)
    nombres = models.CharField(max_length=50)


