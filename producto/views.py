#!usr/local/bin
# coding: latin-1

import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Producto, Marca
from usuario.models import Usuario
from usuario.utils import regex, error_messages
from .forms import ProductoForm, BusquedaForm

# Create your views here.


class CreacionProducto(LoginRequiredMixin, CreateView):

    """
    Crea un nuevo producto.
    """

    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear_producto.html'
    success_url = reverse_lazy('usuario:admin_home')
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
        Se envía al template una variable rol con el rol del usuario, para verificar si el
        usuario puede gestionar(editar y eliminar) los productos de la lista.

        Se obtinen una lista con todos los productos del inventario.
        Se crea una variable 'vacio' la cual determina si la lista de prouctos
        está vacía, para mostrar el respectivo mensaje en el template.
        """

        try:
            self.rol = request.session['rol']
        except KeyError:
            raise PermissionDenied

        context = {
            'form': self.form,
            'marcas': Marca.objects.all(),
            'rol': self.rol,
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

        try:
            prod = self.paginacion.page(page)
        except PageNotAnInteger:
            prod = self.paginacion.page(1)
        except EmptyPage:
            prod = self.pagincacion.page(self.paginacion.num_pages)

        context['productos'] = prod
        context['numero_paginas'] = range(1, self.paginacion.num_pages + 1)

        return render(request, self.template_name, context)

    def post(self, request):
        """
        Se obtiene el rol del usuario para detenmiar si este puede gestionar (editar y eliminar)
        los productos del inventario.
        Se válida la búsqueda del usuario, si es válida se realiza la consulta a la base de datos y se
        verifica que si hubieron resultados. Si búsqueda no es válida se envía el formulario con el
        correspondiente mensaje de error.
        """

        try:
            self.rol = request.session['rol']
        except KeyError:
            raise PermissionDenied

        context = {
            'form': self.form,
            'marcas': Marca.objects.all(),
            'rol': self.rol,
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


class ActualizacionProducto(LoginRequiredMixin, UpdateView):

    """
    Actuailza los datos de un producto.
    """

    model = Producto
    template_name = 'producto/actualizar_producto.html'
    form_class = ProductoForm
    login_url = reverse_lazy('usuario:iniciar_sesion')
    success_url = reverse_lazy('usuario:admin_home')

    def get(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(ActualizacionProducto, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        """
        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(ActualizacionProducto, self).post(request, *args, **kwargs)
        else:
            raise PermissionDenied


class EliminacionProducto(LoginRequiredMixin, DeleteView):

    model = Producto
    success_url = reverse_lazy('usuario:listar_productos')
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def post(self, request, *args, **kwargs):
        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(EliminacionProducto, self).post(request, *args, **kwargs)
        else:
            raise PermissionDenied
