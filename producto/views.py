#!usr/local/bin
# coding: latin-1

import re
import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Producto, Marca, DetalleFactura, Factura
from usuario.models import Usuario
from usuario.utils import regex, get_url, get_namespace, get_objects
from .forms import (
    ProductoForm,
    BusquedaForm,
    BusquedaProductoForm,
    AgregarProductoForm,
    DetalleFacturaForm,
    FacturaForm
)
from usuario.forms import ClienteForm
from usuario.forms import FormBusquedaCliente


class CreacionProducto(LoginRequiredMixin, CreateView):

    """
    Crea un nuevo producto.
    """

    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear_producto.html'
    success_url = reverse_lazy('usuario:admin_listar_productos')
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def get(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que est� intentado acceder a la vista.
        Si el permiso no es v�lido deniega el acceso.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(CreacionProducto, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que est� intentado acceder a la vista.
        Si el permiso no es v�lido deniega el acceso.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(CreacionProducto, self).post(request, *args, **kwargs)
        else:
            raise PermissionDenied


class ListaProducto(LoginRequiredMixin, View):

    """
    Obtiene una lista con todos los productos del inventario.
    """

    MARCA = 'marca'
    ESTILO = 'estilo'
    GENERO = 'genero'

    form = BusquedaForm()
    template_name = 'producto/lista_productos.html'
    login_url = reverse_lazy('usuario:iniciar_sesion')
    rol = filtro = id_filtro = None
    busqueda_filtrada = False
    paginacion = None
    numero_productos = 3

    def get(self, request):
        """
        Se obtinen una lista con todos los productos del inventario.
        Se crea una variable 'vacio' la cual determina si la lista de prouctos
        est� vac�a, para mostrar el respectivo mensaje en el template.

        Verifca el permiso del usuario que est� intentado acceder a la vista.
        Si el permiso no es v�lido deniega el acceso.
        Obtiene la lista de todos los clientes que est�n registrados en el sistema.
        Crea la paginaci�n.

        Se env�a al template la url y el namespace de las urls ListarProductos y EditarProductos, dependiendo del
        usuario que est� realizando la acci�n (Administrador o Vendedor). Est� url
        se utiliza para asignarla a los filtros de b�queda (marca, estilo, g�nero).
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
                request.user.has_perm(Usuario.PERMISO_VENDEDOR):

            context = {
                'form': self.form,
                'marcas': Marca.objects.all(),
                'url_listar_producto': get_url(request, view='listar_productos'),
                'namespace_editar_producto': get_namespace(request, view='editar_producto')
            }

            try:
                self.filtro = request.GET['filtro']
                self.id_filtro = request.GET['id']
                self.busqueda_filtrada = True
            except KeyError:
                pass

            page = request.GET.get('page')

            productos = None

            if self.busqueda_filtrada:
                if self.filtro == ListaProducto.MARCA:
                    if re.match(regex['numero'], self.id_filtro):
                        productos = Producto.objects.filter(marca=self.id_filtro)
                elif self.filtro == ListaProducto.ESTILO:
                    if re.match(regex['estilo'], self.id_filtro):
                        productos = Producto.objects.filter(estilo=self.id_filtro)
                        print productos
                elif self.filtro == ListaProducto.GENERO:
                    if re.match(regex['genero'], self.id_filtro):
                        productos = Producto.objects.filter(genero=self.id_filtro)

                if productos is not None:
                    context['resultados'] = len(productos)
                else:
                    context['error_busqueda'] = u'El filtro de b�squeda no es v�lido.'
            else:
                productos = Producto.objects.all()
                vacio = True if len(productos) == 0 else False
                context['vacio'] = vacio

            self.paginacion = Paginator(productos, self.numero_productos)

            prod = get_objects(self.paginacion, page)

            context['productos'] = prod
            context['numero_paginas'] = range(1, self.paginacion.num_pages + 1)

            return render(request, self.template_name, context)
        else:
            raise PermissionDenied

    def post(self, request):
        """
        Se v�lida la b�squeda del usuario, si es v�lida se realiza la consulta a la base de datos y se
        verifica que si hubieron resultados. Si b�squeda no es v�lida se env�a el formulario con el
        correspondiente mensaje de error.

        Verifca el permiso del usuario que est� intentado acceder a la vista.
        Si el permiso no es v�lido deniega el acceso.
        Obtiene la lista de todos los clientes que est�n registrados en el sistema.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
                request.user.has_perm(Usuario.PERMISO_VENDEDOR):

            context = {
                'form': self.form,
                'marcas': Marca.objects.all(),
                'url_listar_producto': get_url(request, view='listar_productos'),
                'namespace_editar_producto': get_namespace(request, view='editar_producto')
            }

            self.form = BusquedaForm(data=request.POST)

            if self.form.is_valid():
                id_referencia = self.form.cleaned_data.get('busqueda')
                productos = Producto.objects.filter(id_referencia=id_referencia)
                context['resultados'] = len(productos)
                context['productos'] = productos
            else:
                context['error_form'] = True

            context['form'] = self.form

            return render(request, self.template_name, context)
        else:
            raise PermissionDenied


class ActualizacionProducto(LoginRequiredMixin, UpdateView):

    """
    Actuailza los datos de un producto.
    """

    model = Producto
    template_name = 'producto/actualizar_producto.html'
    form_class = ProductoForm
    login_url = reverse_lazy('usuario:iniciar_sesion')
    success_url = reverse_lazy('usuario:admin_listar_productos')

    def get(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que est� intentado acceder a la vista.
        Si el permiso no es v�lido deniega el acceso.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(ActualizacionProducto, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que est� intentado acceder a la vista.
        Si el permiso no es v�lido deniega el acceso.
        Dependiendo del tipo de usuario que est� realizando la petici�n, se define la
        url a donde ser� redirigido una vez se hayan actualizado los datos.
        """
        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(ActualizacionProducto, self).post(request, *args, **kwargs)
        else:
            raise PermissionDenied


class EliminacionProducto(LoginRequiredMixin, DeleteView):
    """
    Permite al usuario Administrador eliminar los productos del inventario.
    """

    model = Producto
    success_url = reverse_lazy('usuario:admin_listar_productos')
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def get(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que est� intentado acceder a la vista.
        Si el permiso no es v�lido deniega el acceso.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(EliminacionProducto, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que est� intentado acceder a la vista.
        Si el permiso no es v�lido deniega el acceso.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(EliminacionProducto, self).post(request, *args, **kwargs)
        else:
            raise PermissionDenied


class Facturacion(LoginRequiredMixin, View):

    template_name = 'factura/crear_factura.html'
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def get(self, request):
        if request.user.has_perm(Usuario.PERMISO_VENDEDOR):
            context = {
                'form_cliente': FormBusquedaCliente(),
                'form_producto': BusquedaProductoForm(),
                'form': ClienteForm(),
                'agregar_cliente': True,
                'vendedor': Usuario.objects.get(user=request.user)
            }

            return render(request, self.template_name, context)
        else:
            raise PermissionDenied

    def post(self, request):
        if request.user.has_perm(Usuario.PERMISO_VENDEDOR):
            datos = json.loads(request.body)

            datos_factura = {
                "cliente": datos.get('cliente'),
                "vendedor": request.user.id
            }
            factura_form = FacturaForm(data=datos_factura)

            detalle_factura = datos.get('detalle')
            valido = True

            if factura_form.is_valid():
                factura = factura_form.save()

                total_pagar = 0

                for detalle in detalle_factura:
                    detalle['factura'] = unicode(factura.id)
                    detalle_form = DetalleFacturaForm(data=detalle)

                    if detalle_form.is_valid():
                        nuevo_detalle = detalle_form.save(commit=False)

                        nuevo_detalle.total = nuevo_detalle.cantidad * nuevo_detalle.producto.precio
                        nuevo_detalle.producto.stock -= nuevo_detalle.cantidad
                        nuevo_detalle.producto.save()
                        nuevo_detalle.save()

                        total_pagar += nuevo_detalle.total
                    else:
                        valido = False
                        break

                factura.total_pagar = total_pagar
                factura.save()
            else:
                valido = False

            if valido:
                response = {
                    "response": "success",
                    "mensaje": u"La factura ha sido guardada correctamente.",
                    "url": unicode(reverse_lazy('usuario:vendedor_ver_factura', kwargs={'pk': factura.id}))
                }
            else:
                response = {
                    "response": "error",
                    "mensaje": u'<b>Error: </b>Ocurrio un error al procesar la solicitud.'
                }

            return HttpResponse(json.dumps(response))
        else:
            raise PermissionDenied


class ListaFactura(LoginRequiredMixin, View):

    """
    Lista todas las facturas.
    """

    template_name = 'factura/lista_facturas.html'
    numero_paginas = 4
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def get(self, request):
        if request.user.has_perm(Usuario.PERMISO_ADMIN) \
                or request.user.has_perm(Usuario.PERMISO_VENDEDOR):
            pagina = request.GET.get('page')
            paginacion = Paginator(Factura.objects.all(), self.numero_paginas)

            context = {
                'facturas': get_objects(paginacion, pagina),
                'numero_paginas': range(1, paginacion.num_pages + 1)
            }

            return render(request, self.template_name, context)
        else:
            raise PermissionDenied


def calcular_total_factura(detalles):
    subtotal = 0

    for detalle in detalles:
        subtotal += (detalle.cantidad * detalle.producto.precio)

    iva = subtotal * 0.19

    total = {
        'subtotal': subtotal,
        'iva': iva,
        'total_pagar': subtotal + iva
    }

    return total


class Comprobante(LoginRequiredMixin, View):

    template_name = 'factura/comprobante.html'
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def get(self, request, *args, **kwargs):
        if request.user.has_perm(Usuario.PERMISO_ADMIN) \
                or request.user.has_perm(Usuario.PERMISO_VENDEDOR):
            factura = get_object_or_404(Factura, id=kwargs.get('pk'))

            detalles = DetalleFactura.objects.filter(factura=factura)
            total = calcular_total_factura(detalles)

            context = {
                'factura': factura,
                'detalles': detalles,
                'subtotal': total.get('subtotal'),
                'iva': total.get('iva'),
                'total_pagar': total.get('total_pagar')
            }

            return render(request, self.template_name, context)
        else:
            raise PermissionDenied


def buscar_producto(request):
    if request.user.has_perm(Usuario.PERMISO_VENDEDOR):
        if request.method == 'POST':
            datos = json.loads(request.body)
            print datos
            form = BusquedaProductoForm(data=datos)

            if form.is_valid():
                try:
                    producto = Producto.objects.get(id_referencia=form.cleaned_data.get('referencia'))
                except ObjectDoesNotExist:
                    producto = None

                if producto is not None:
                    response = {
                        'response': 'success',
                        'id': producto.id,
                        'referencia': producto.id_referencia,
                        'nombre': producto.nombre,
                        'marca': producto.marca.nombre,
                        'precio': producto.precio,
                        'stock': producto.stock
                    }
                else:
                    response = {
                        'response': 'empty',
                        'mensaje': u'El producto no existe.'
                    }
            else:
                response = {
                    'response': 'error_form',
                    'mensaje': form.errors['referencia'][0]
                }

            return HttpResponse(json.dumps(response))

    else:
        raise PermissionDenied
