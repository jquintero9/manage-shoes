from django.conf.urls import url
from django.views.generic import TemplateView
from .views import (
    InicioSesion,
    RegistroVendedor,
    cerrar_sesion,
)

urlpatterns = [
    url(r'^$', InicioSesion.as_view(), name='iniciar_sesion'),
    url(r'^usuario/admin$',
        TemplateView.as_view(template_name='usuario/admin/home.html'), name='admin_home'),
    url(r'^usuario/vendedor$',
        TemplateView.as_view(template_name='usuario/vendedor/home.html'), name='vendedor_home'),
    url(r'^cuentas/registrar$', RegistroVendedor.as_view(), name='registrar_vendedor'),
    url(r'^cuentas/registrar$', RegistroVendedor.as_view(), name='registrar_vendedor'),
    url(r'^cuentas/registrar/success$',
        TemplateView.as_view(template_name='usuario/autenticacion/registro_success.html'),
        name='registro_success'),
    url(r'^cuentas/logout$', cerrar_sesion, name='cerrar_sesion'),
]
