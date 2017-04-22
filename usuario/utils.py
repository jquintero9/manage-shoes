#! usr/bin/local
# coding: latin-1

regex = {
    'texto': r'^[A-Za-z����������\s]+$',
    'rol': r'^(administrador|vendedor)$',
    'cedula': r'^[0-9]+{10,10}$',
    'direccion': r'^[a-zA-Z0-9#\-\s]$',
    'telefono': r'([3]([0][0-5]|[1][0-9]|[2][0-2]|[5][01])[\d]{7})|([2-8][\d]{6,6})$',
    'password': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&#\-_])[A-Za-z\d$@$!%*?&#\-_]{8,16}',
}

error_messages = {
    'texto': u'Ingrese solo letras.',
    'rol': u'El rol no es v�lido',
    'cedula': u'Solo se admiten n�meros.',
    'direccion': u'El formato de la direcci�n no es v�lido.',
    'telefono': u'El n�mero ingresado no es v�lido.',
    'password': u'La contrase�a debe tener m�ximo un caracter especial($@$!%*?&), '
                u'una minusc�la, una mayusc�la y un d�gito.'
}