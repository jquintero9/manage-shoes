#!usr/bin/local
# coding: latin-1

"""
Esta es la configuraci�n para ejecutar la aplicaci�n en producci�n
"""


"""
Se importa la configuraci�n de la aplicacip�n para obtener
la instancia de la base de datos que est� utilizando la aplicaci�n.
"""
from django.conf import settings

"""
dj_database_url: Realiza una sincronizaci�n entre la base de datos
de la aplicaci�n y la base de datos del servidor (Heroku)
"""
import dj_database_url

"""Se desactiva el modo debug de la aplicaci�n, para que no muestre
informaci�n detallada en caso de que ocurra un error."""
DEBUG = False

DATABASES = settings.DATABASES

db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES['default'].update(db_from_env)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

STATICFILES_STORAGE = 'whithenoise.django.GzipManifestStaticFilesStorage'
