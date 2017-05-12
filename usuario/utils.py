#! usr/bin/local
# coding: latin-1

from django.template import loader
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.urls import reverse_lazy

regex = {
    'texto': r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$',
    'rol': r'^(administrador|vendedor)$',
    'cedula': r'^[0-9]{10}$',
    'direccion': r'^[a-zA-Z0-9#\-\s]+$',
    'telefono': r'^([3]([0][0-5]|[1][0-9]|[2][0-2]|[5][01])[0-9]{7})|([2-8][0-9]{6})$',
    'password': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&#\-_])[A-Za-z\d$@$!%*?&#\-_]{8,16}',
    'id_referencia': r'^[A-Za-z0-9]{6}$',
    'nombre_producto': r'^[A-Za-z0-9\s]+$',
    'genero': r'^hombre|mujer|unisex$',
    'estilo': r'^deportivo|formal$',
    'talla': r'^2[7-9]|3[0-9]|4[0-3]$',
    'numero': r'^[0-9]+$'
}

error_messages = {
    'texto': u'Ingrese solo letras.',
    'rol': u'El rol no es válido',
    'cedula': u'Número de cédula no válido.',
    'direccion': u'El formato de la dirección no es válido.',
    'telefono': u'El número de teléfono no es válido.',
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

    try:
        send_mail(
            subject=subject,
            message='Tu cuenta ha sido activada.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=True,
            html_message=html_message
        )
    except:
        pass


def get_prefix(request):
    if request.session.get('rol') == 'administrador':
        prefix = 'admin'
    elif request.session.get('rol') == 'vendedor':
        prefix = 'vendedor'

    return prefix


def get_url(request, view):
    prefix = get_prefix(request)

    if view == 'listar_productos':
        url = reverse_lazy('usuario:' + prefix + '_listar_productos')
    elif view == 'listar_clientes':
        url = reverse_lazy('usuario:' + prefix + '_listar_clientes')

    return url


def get_namespace(request, view):
    prefix = get_prefix(request)

    if view == 'editar_producto':
        namespace = 'usuario:' + prefix + '_editar_producto'
    elif view == 'editar_cliente':
        namespace = 'usuario:' + prefix + '_editar_cliente'

    return namespace


def get_objects(paginacion, page):

    try:
        objetos = paginacion.page(page)
    except PageNotAnInteger:
        objetos = paginacion.page(1)
    except EmptyPage:
        objetos = paginacion.page(paginacion.num_pages)

    return objetos
