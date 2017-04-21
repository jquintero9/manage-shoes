#usr/bin/local
# coding: latin-1

"""
WSGI config for manage_shoes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manage_shoes.settings")

"""
Esta libreria de python whitenoise permite gestionar el almacenamiento
de los archivos estaticos de la aplicación.
"""
from whitenoise.django import DjangoWhiteNoise


application = get_wsgi_application()

application = DjangoWhiteNoise(application)
