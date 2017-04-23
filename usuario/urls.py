from django.conf.urls import url
from django.views.generic import TemplateView
from .views import (
    InicioSesion,
    RegistroVendedor,
    cerrar_sesion,
    ActivacionCuentas,
    HomeAdmin,
    HomeVendedor,
)

urlpatterns = [
    url(r'^$', InicioSesion.as_view(), name='iniciar_sesion'),
    url(r'^usuario/admin$', HomeAdmin.as_view(), name='admin_home'),
    url(r'^usuario/admin/activar-cuentas$', ActivacionCuentas.as_view(), name='activar_cuentas'),
    url(r'^usuario/vendedor$', HomeVendedor.as_view(), name='vendedor_home'),
    url(r'^cuentas/registrar$', RegistroVendedor.as_view(), name='registrar_vendedor'),
    url(r'^cuentas/registrar/success$',
        TemplateView.as_view(template_name='usuario/autenticacion/registro_success.html'),
        name='registro_success'),
    url(r'^cuentas/logout$', cerrar_sesion, name='cerrar_sesion'),
]
