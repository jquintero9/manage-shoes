#!usr/local/bin
# coding: latin-1

import re
import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Producto, Marca
from usuario.models import Usuario
from usuario.utils import regex, get_url, get_namespace, get_objects
from .forms import ProductoForm, BusquedaForm, BusquedaProductoForm
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
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(CreacionProducto, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
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
        está vacía, para mostrar el respectivo mensaje en el template.

        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        Obtiene la lista de todos los clientes que están registrados en el sistema.
        Crea la paginación.

        Se envía al template la url y el namespace de las urls ListarProductos y EditarProductos, dependiendo del
        usuario que esté realizando la acción (Administrador o Vendedor). Está url
        se utiliza para asignarla a los filtros de búqueda (marca, estilo, género).
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
                    context['error_busqueda'] = u'El filtro de búsqueda no es válido.'
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
        Se válida la búsqueda del usuario, si es válida se realiza la consulta a la base de datos y se
        verifica que si hubieron resultados. Si búsqueda no es válida se envía el formulario con el
        correspondiente mensaje de error.

        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        Obtiene la lista de todos los clientes que están registrados en el sistema.
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

    def get(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN) or request.user.has_perm(Usuario.PERMISO_VENDEDOR):
            return super(ActualizacionProducto, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        Dependiendo del tipo de usuario que esté realizando la petición, se define la
        url a donde será redirigido una vez se hayan actualizado los datos.
        """
        if request.user.has_perm(Usuario.PERMISO_ADMIN) or request.user.has_perm(Usuario.PERMISO_VENDEDOR):

            if request.session.get('rol') == Usuario.ADMIN:
                self.success_url = reverse_lazy('usuario:admin_listar_productos')
            elif request.session.get('rol') == Usuario.VENDEDOR:
                self.success_url = reverse_lazy('usuario:vendedor_listar_productos')

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
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(EliminacionProducto, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(EliminacionProducto, self).post(request, *args, **kwargs)
        else:
            raise PermissionDenied


def crear_factura(request):

    context = {
        'form_cliente': FormBusquedaCliente(),
        'form_producto': BusquedaProductoForm(),
        'form': ClienteForm(),
        'agregar_cliente': True
    }

    return render(request, 'factura/crear_factura.html', context)


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
