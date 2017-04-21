#! usr/bin/local
# coding: latin-1

regex = {
    'texto': r'^[A-Za-záéíóúÁÉÍÓÚ\s]+$',
    'rol': r'^(administrador|vendedor)$',
    'cedula': r'^[0-9]+{10,10}$',
    'dirección': r'^[a-zA-Z0-9#\-\s]$',
    'telefono': r'^$',
}

error_messages = {
    'texto': u'Ingrese solo letras.',
    'rol': u'El rol no es válido',
    'cedula': u'Solo se admiten números.',
    'direccion': u'El formato de la dirección no es válido.',
    'telefono': u'El número ingresado no es válido.',
}
