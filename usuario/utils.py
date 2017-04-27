#! usr/bin/local
# coding: latin-1

from django.template import loader
from django.core.mail import send_mail
from django.conf import settings

regex = {
    'texto': r'^[A-Za-záéíóúÁÉÍÓÚ\s]+$',
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
    'rol': u'El rol no es válido',
    'cedula': u'Solo se admiten números.',
    'direccion': u'El formato de la dirección no es válido.',
    'telefono': u'El número ingresado no es válido.',
    'password': u'La contraseña debe tener máximo un caracter especial($@$!%*?&), '
                u'una minuscúla, una mayuscúla y un dígito.',
    'id_referencia': u'El formato del ID no es válido',
    'nombre_producto': u'Ingrese solo caracteres alfanumericos',
    'genero': u'El género no es válido.',
    'estilo': u'El estilo no es válido',
    'talla': u'El número de tall no es válido',
    'numero': u'Ingrese solo números.'
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
