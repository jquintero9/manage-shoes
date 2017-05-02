from django.conf.urls import url
from django.views.generic import TemplateView
from .views import (
    InicioSesion,
    RegistroVendedor,
    RegistroCliente,
    ActualizacionCliente,
    EliminacionCliente,
    ListaCliente,
    cerrar_sesion,
    ActivacionCuentas,
    HomeAdmin,
    HomeVendedor,
    buscar_cliente,
)

from producto.views import (
    CreacionProducto,
    ListaProducto,
    ActualizacionProducto,
    EliminacionProducto,
    crear_factura,
)

urlpatterns = [
    url(r'^$', InicioSesion.as_view(), name='iniciar_sesion'),
    url(r'^usuario/admin$', HomeAdmin.as_view(), name='admin_home'),
    url(r'^usuario/admin/activar-cuentas$', ActivacionCuentas.as_view(), name='activar_cuentas'),
    url(r'^usuario/admin/producto/crear$', CreacionProducto.as_view(), name='crear_producto'),
    url(r'^usuario/admin/producto/(?P<pk>\d+)/editar$', ActualizacionProducto.as_view(), name='admin_editar_producto'),
    url(r'^usuario/admin/producto/(?P<pk>\d+)/eliminar$', EliminacionProducto.as_view(), name='eliminar_producto'),
    url(r'^usuario/admin/producto/lista$', ListaProducto.as_view(), name='admin_listar_productos'),
    url(r'^usuario/admin/cliente/crear$', RegistroCliente.as_view(), name='admin_registrar_cliente'),
    url(r'^usuario/admin/cliente/lista$', ListaCliente.as_view(), name='admin_listar_clientes'),
    url(r'^usuario/admin/cliente/(?P<pk>\d+)/editar$', ActualizacionCliente.as_view(), name='admin_editar_cliente'),
    url(r'^usuario/admin/cliente/(?P<pk>\d+)/eliminar$', EliminacionCliente.as_view(), name='eliminar_cliente'),
    url(r'^usuario/vendedor$', HomeVendedor.as_view(), name='vendedor_home'),
    url(r'^usuario/vendedor/producto/lista$', ListaProducto.as_view(), name='vendedor_listar_productos'),
    url(r'^usuario/vendedor/producto/(?P<pk>\d+)/editar$',
        ActualizacionProducto.as_view(), name='vendedor_editar_producto'),
    url(r'^usuario/vendedor/cliente/crear$', RegistroCliente.as_view(), name='vendedor_registrar_cliente'),
    url(r'^usuario/vendedor/cliente/lista$', ListaCliente.as_view(), name='vendedor_listar_clientes'),
    url(r'^usuario/vendedor/cliente/(?P<pk>\d+)/editar$',
        ActualizacionCliente.as_view(), name='vendedor_editar_cliente'),
    url(r'^usuario/vendedor/factura/crear$', crear_factura, name='crear_factura'),
    url(r'^usuario/vendedor/factura/buscar-cliente$', buscar_cliente, name='buscar_cliente'),
    url(r'^cuentas/registrar$', RegistroVendedor.as_view(), name='registrar_vendedor'),
    url(r'^cuentas/registrar/success$',
        TemplateView.as_view(template_name='usuario/autenticacion/registro_success.html'),
        name='registro_success'),
    url(r'^cuentas/logout$', cerrar_sesion, name='cerrar_sesion'),
]
