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

from producto.views import (
    CreacionProducto,
    ListaProducto,
    ActualizacionProducto,
    EliminacionProducto,
)

urlpatterns = [
    url(r'^$', InicioSesion.as_view(), name='iniciar_sesion'),
    url(r'^usuario/admin$', HomeAdmin.as_view(), name='admin_home'),
    url(r'^usuario/admin/activar-cuentas$', ActivacionCuentas.as_view(), name='activar_cuentas'),
    url(r'^usuario/admin/producto/crear$', CreacionProducto.as_view(), name='crear_producto'),
    url(r'^usuario/admin/producto/(?P<pk>\d+)/editar', ActualizacionProducto.as_view(), name='actualizar_producto'),
    url(r'^usuario/admin/producto/(?P<pk>\d+)/eliminar', EliminacionProducto.as_view(), name='eliminar_producto'),
    url(r'^usuario/admin/producto/lista$', ListaProducto.as_view(), name='listar_productos'),
    url(r'^usuario/vendedor$', HomeVendedor.as_view(), name='vendedor_home'),
    url(r'^cuentas/registrar$', RegistroVendedor.as_view(), name='registrar_vendedor'),
    url(r'^cuentas/registrar/success$',
        TemplateView.as_view(template_name='usuario/autenticacion/registro_success.html'),
        name='registro_success'),
    url(r'^cuentas/logout$', cerrar_sesion, name='cerrar_sesion'),
]
