#! usr/bin/local
# coding: latin-1

regex = {
    'texto': r'^[A-Za-z����������\s]+$',
    'rol': r'^(administrador|vendedor)$',
    'cedula': r'^[0-9]+{10,10}$',
    'direcci�n': r'^[a-zA-Z0-9#\-\s]$',
    'telefono': r'^$',
}

error_messages = {
    'texto': u'Ingrese solo letras.',
    'rol': u'El rol no es v�lido',
    'cedula': u'Solo se admiten n�meros.',
    'direccion': u'El formato de la direcci�n no es v�lido.',
    'telefono': u'El n�mero ingresado no es v�lido.',
}
