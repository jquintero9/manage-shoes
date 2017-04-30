#!usr/local/bin
# coding: latin-1

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import (
    UserForm,
    UsuarioForm,
    LoginForm,
    ClienteForm,
    DepartamentoForm,
    BusquedaClienteForm
)
from .models import Usuario, Cliente
from .utils import enviar_email


class RegistroVendedor(View):

    """
    Registra un usuario vendedor.
    """

    template_name = 'usuario/autenticacion/registrar_vendedor.html'
    user_form = usuario_form = None

    def get(self, request):

        """
        Procesa la petici�n HTTP por el m�todo GET.
        :param request: Contiene la informaci�n de la petici�n HTTP.
        :return: La vista Registrar Vendedor.
        """

        self.user_form = UserForm()
        self.usuario_form = UsuarioForm()

        context = {
            'user_form': self.user_form,
            'usuario_form': self.usuario_form
        }

        return render(request, self.template_name, context)

    def post(self, request):

        """
        Procesa los datos que son recibidos desde el formulario, por
        el m�todo POST.
        Primero de validan los datos del formulario user_form y luego se crea la instancia
        del modelo User. Posteriormente se v�lida el formulario usuario_form y luego se crea
        la instancia del modelo Usuario y se agrega el permiso correspondiente.
        :param request: Contiene la informaci�n que fuen enviada mediante la
        petici�n HTTP.
        :return: Redireccionada al ususario a otra vista dependiendo del resultado
        de la validaci�n.
        """

        self.user_form = UserForm(data=request.POST)
        self.usuario_form = UsuarioForm(data=request.POST)

        if self.user_form.is_valid() and self.usuario_form.is_valid():
            '#Se crea la instancia del modelo User'
            print self.user_form.cleaned_data.get('password')
            user = User.objects.create_user(
                username=self.user_form.cleaned_data.get('email'),
                password=self.user_form.cleaned_data.get('password'),
                email=self.user_form.cleaned_data.get('email')
            )

            permiso_vendedor = Permission.objects.get(name='es vendedor')
            user.user_permissions.add(permiso_vendedor)

            user.save()

            vendedor = Usuario(
                user=user,
                nombres=self.usuario_form.cleaned_data.get('nombres'),
                apellidos=self.usuario_form.cleaned_data.get('apellidos'),
                rol=self.usuario_form.cleaned_data.get('rol')
            )

            vendedor.save()

            return HttpResponseRedirect(reverse_lazy('usuario:registro_success'))
        else:
            context = {
                'user_form': self.user_form,
                'usuario_form': self.usuario_form
            }

            return render(request, self.template_name, context)


class RegistroCliente(LoginRequiredMixin, CreateView):

    model = Cliente
    template_name = 'usuario/cliente/crear_cliente.html'
    login_url = reverse_lazy('usuario:iniciar_sesion')
    form_class = ClienteForm

    def get_context_data(self, **kwargs):
        context = super(RegistroCliente, self).get_context_data(**kwargs)
        context['form_departamento'] = DepartamentoForm()

        return context

    def get(self, request, *args, **kwargs):
        if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
                request.user.has_perm(Usuario.PERMISO_VENDEDOR):
            return super(RegistroCliente, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
                request.user.has_perm(Usuario.PERMISO_VENDEDOR):

            try:
                if request.session['rol'] == Usuario.ADMIN:
                    self.success_url = reverse_lazy('usuario:admin_home')
                elif request.session['rol'] == Usuario.VENDEDOR:
                    self.success_url = reverse_lazy('')
            except KeyError:
                pass

            return super(RegistroCliente, self).post(request, *args, **kwargs)
        else:
            raise PermissionDenied


class ListaCliente(LoginRequiredMixin, View):

    template_name = 'usuario/cliente/lista_clientes.html'
    login_url = reverse_lazy('usuario:iniciar_sesion')
    paginacion = None
    numero_clientes = 1

    def get(self, request):
        if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
                request.user.has_perm(Usuario.PERMISO_VENDEDOR):

            context = {'form': BusquedaClienteForm()}

            page = request.GET.get('page')

            self.paginacion = Paginator(Cliente.objects.all(), self.numero_clientes)

            try:
                clientes = self.paginacion.page(page)
            except PageNotAnInteger:
                clientes = self.paginacion.page(1)
            except EmptyPage:
                clientes = self.paginacion.page(self.paginacion.num_pages)

            context['clientes'] = clientes
            context['numero_paginas'] = range(1, self.paginacion.num_pages + 1)

            return render(request, self.template_name, context)
        else:
            raise PermissionDenied

    def post(self, request):
        if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
                request.user.has_perm(Usuario.PERMISO_VENDEDOR):
            form = BusquedaClienteForm(data=request.POST)
            context = {'form': form, 'breadcrumb': 'clientes'}

            if form.is_valid():
                cedula = form.cleaned_data.get('busqueda')
                clientes = Cliente.objects.filter(cedula=cedula)
                context['clientes'] = clientes
                context['resultado'] = len(clientes)

            return render(request, self.template_name, context)
        else:
            raise PermissionDenied


class ActualizacionCliente(LoginRequiredMixin, UpdateView):

    model = Cliente
    template_name = 'usuario/cliente/actualizar_cliente.html'
    form_class = ClienteForm
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def get(self, request, *args, **kwargs):
        if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
                request.user.has_perm(Usuario.PERMISO_VENDEDOR):

            return super(ActualizacionCliente, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
                request.user.has_perm(Usuario.PERMISO_VENDEDOR):

            try:
                if request.session['rol'] == Usuario.ADMIN:
                    self.success_url = reverse_lazy('usuario:admin_home')
                elif request.session['rol'] == Usuario.VENDEDOR:
                    self.success_url = reverse_lazy('')
            except KeyError:
                pass

            return super(ActualizacionCliente, self).post(request, *args, **kwargs)
        else:
            raise PermissionDenied


class EliminacionCliente(LoginRequiredMixin, DeleteView):

    model = Cliente
    login_url = reverse_lazy('usuario:iniciar_sesion')
    success_url = reverse_lazy('usuario:listar_clientes')

    def post(self, request, *args, **kwargs):
        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(EliminacionCliente, self).post(request, *args, **kwargs)
        else:
            raise PermissionDenied


class InicioSesion(View):

    """
    Auntentica los usuairos de tipo Administrador y Vendedor.
    """

    template_name = 'usuario/autenticacion/iniciar_sesion.html'
    form_class = None
    success_url = None

    def get(self, request):

        """
        Procesa la petici�n HTTP por el m�todo GET.
        Se instancia el formulario de inicio de sesi�n y se env�a
        al template.
        Si ya hay una sesi�n iniciada entonces se redirige al usuario a su vista correspondiente.
        :param request: Contiene la informaci�n de la petici�n HTTP.
        :return: La vista Registrar Vendedor.
        """

        if not request.user.is_authenticated():

            self.form_class = LoginForm()
            context = {'form': self.form_class}

            return render(request, self.template_name, context)
        else:
            try:
                if request.session['rol'] == Usuario.ADMIN:
                    redirect_url = reverse_lazy('usuario:admin_home')
                elif request.session['rol'] == Usuario.VENDEDOR:
                    redirect_url = reverse_lazy('usuario:vendedor_home')

                return HttpResponseRedirect(redirect_url)
            except KeyError:
                return HttpResponseRedirect(reverse_lazy('usuario:iniciar_sesion'))

    def post(self, request):

        """
        Procesa los datos que llengan por el formulario mediante el
        m�todo POST.
        Se instancia el formulario de Inicio de Sesi�n, para validar los datos.
        Luego se verifica el estado de la cuenta del usuario, su est� activa
        Se crea la sesi�n y se redirecciona a su respectiva vista y de lo contrario
        no se permite el acceso a la aplicaci�n.

        :param request: Contiene la informaci�n de la petici�n HTTP.
        :return: Se redirecciona a la vista del usuairo o se retorna el formulario.
        """

        self.form_class = LoginForm(data=request.POST)

        if self.form_class.is_valid():
            correo = self.form_class.cleaned_data.get('email')
            password = self.form_class.cleaned_data.get('password')

            user = authenticate(username=correo, password=password)

            if user is not None:
                usuario = Usuario.objects.get(user=user)
                if usuario.activo:
                    login(request, user=user)
                    request.session['rol'] = usuario.rol

                    if user.has_perm(Usuario.PERMISO_ADMIN):
                        self.success_url = reverse_lazy('usuario:admin_home')
                    elif user.has_perm(Usuario.PERMISO_VENDEDOR):
                        self.success_url = reverse_lazy('usuario:vendedor_home')
                    return HttpResponseRedirect(self.success_url)
                else:
                    messages.warning(request, u'Esta cuenta no est� activa.')
            else:
                messages.error(request, u'El correo y/o la contrase�a no coinciden.')

        context = {'form': self.form_class}

        return render(request, self.template_name, context)


class ActivacionCuentas(LoginRequiredMixin, View,):

    """
    Permite activar las cuentas de los usuarios Vendedores.
    """

    template_name = 'usuario/admin/activar_cuentas.html'
    activo = 'on'
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def get(self, request):

        if request.user.has_perm(Usuario.PERMISO_ADMIN):

            usuarios_inactivos = Usuario.objects.filter(activo=False)

            context = {'usuarios': usuarios_inactivos}

            return render(request, self.template_name, context)
        else:
            raise PermissionDenied

    def post(self, request):
        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            data = request.POST.items()

            for email, switch in data:
                if not email == 'csrfmiddlewaretoken':
                    user = get_object_or_404(klass=User, username=email)
                    usuario = get_object_or_404(klass=Usuario, user=user)

                    if switch == self.activo:
                        usuario.activo = True
                        usuario.save()
                        enviar_email(user.username, usuario.nombre_completo())

            messages.success(request, u'Las cuentas han sido activadas correctamente.')
            return HttpResponseRedirect(reverse_lazy('usuario:admin_home'))
        else:
            raise PermissionDenied


class HomeAdmin(LoginRequiredMixin, View):

    template_name = 'usuario/admin/home.html'
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def get(self, request):
        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return render(request, self.template_name, {})
        else:
            raise PermissionDenied


class HomeVendedor(LoginRequiredMixin, View):

    template_name = 'usuario/vendedor/home.html'
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def get(self, request):
        if request.user.has_perm(Usuario.PERMISO_VENDEDOR):
            return render(request, self.template_name, {})
        else:
            raise PermissionDenied


@login_required(login_url=reverse_lazy('usuario:iniciar_sesion'))
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('usuario:iniciar_sesion'))
