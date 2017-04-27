#! usr/bin/local
# coding: latin-1

from django.template import loader
from django.core.mail import send_mail
from django.conf import settings

regex = {
    'texto': r'^[A-Za-z����������\s]+$',
    'rol': r'^(administrador|vendedor)$',
    'cedula': r'^[0-9]+{10,10}$',
    'direccion': r'^[a-zA-Z0-9#\-\s]$',
    'telefono': r'([3]([0][0-5]|[1][0-9]|[2][0-2]|[5][01])[\d]{7})|([2-8][\d]{6,6})$',
    'password': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&#\-_])[A-Za-z\d$@$!%*?&#\-_]{8,16}',
    'id_referencia': r'^[A-Za-z0-9]{6}$',
    'nombre_producto': r'^[A-Za-z0-9]+$',
    'genero': r'^hombre|mujer|unisex$',
    'estilo': r'^deportivo|formal$',
    'talla': r'^[27-43]$',
    'numero': r'^d+$'
}

error_messages = {
    'texto': u'Ingrese solo letras.',
    'rol': u'El rol no es v�lido',
    'cedula': u'Solo se admiten n�meros.',
    'direccion': u'El formato de la direcci�n no es v�lido.',
    'telefono': u'El n�mero ingresado no es v�lido.',
    'password': u'La contrase�a debe tener m�ximo un caracter especial($@$!%*?&), '
                u'una minusc�la, una mayusc�la y un d�gito.',
    'id_referencia': u'El formato del ID no es v�lido',
    'nombre_producto': u'Ingrese solo caracteres alfanumericos',
    'genero': u'El g�nero no es v�lido.',
    'estilo': u'El estilo no es v�lido',
    'talla': u'El n�mero de tall no es v�lido',
    'numero': u'Ingrese solo n�meros.'
}


def enviar_email(email, nombre):

    html_message = loader.render_to_string(
        'usuario/autenticacion/email.html',
        {
            'nombre': nombre,
        }
    )

    subject = 'Manage Shoes - Tu cuenta ha sido activada.'

    send_mail(
        subject=subject,
        message='Tu cuenta ha sido activada.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True,
        html_message=html_message
    )
