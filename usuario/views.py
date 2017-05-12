#!usr/local/bin
# coding: latin-1

import json
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from .forms import (
    UserForm,
    UsuarioForm,
    LoginForm,
    ClienteForm,
    BusquedaClienteForm,
    FormBusquedaCliente,
)
from producto.forms import FacturaForm
from .models import Usuario, Cliente
from .utils import enviar_email, get_namespace, get_objects


class RegistroVendedor(View):

    """
    Registra un usuario vendedor.
    """

    template_name = 'usuario/autenticacion/registrar_vendedor.html'
    user_form = usuario_form = None

    def get(self, request):

        """
        Procesa la petición HTTP por el método GET.
        :param request: Contiene la información de la petición HTTP.
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
        el método POST.
        Primero de validan los datos del formulario user_form y luego se crea la instancia
        del modelo User. Posteriormente se válida el formulario usuario_form y luego se crea
        la instancia del modelo Usuario y se agrega el permiso correspondiente.
        :param request: Contiene la información que fuen enviada mediante la
        petición HTTP.
        :return: Redireccionada al ususario a otra vista dependiendo del resultado
        de la validación.
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

    """
    Permite a los usuarios Administrador y Vendedor registrar nuevos clientes
    en el sistema.
    """

    model = Cliente
    template_name = 'usuario/cliente/crear_cliente.html'
    login_url = reverse_lazy('usuario:iniciar_sesion')
    form_class = ClienteForm

    def get(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
                request.user.has_perm(Usuario.PERMISO_VENDEDOR):
            return super(RegistroCliente, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        Dependiendo del usuario (Administrador o Vendedor) que esté creando el cliente,
        se define la url a la cual será redirigido una vez se halla guardado el nuevo registro.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
                request.user.has_perm(Usuario.PERMISO_VENDEDOR):

            if request.session.get('rol') == Usuario.ADMIN:
                self.success_url = reverse_lazy('usuario:admin_listar_clientes')
            elif request.session.get('rol') == Usuario.VENDEDOR:
                self.success_url = reverse_lazy('usuario:vendedor_listar_clientes')

            return super(RegistroCliente, self).post(request, *args, **kwargs)
        else:
            raise PermissionDenied


class ListaCliente(LoginRequiredMixin, View):
    """
    Obtiene una lista con los clientes que están registrados en sistema.
    """

    template_name = 'usuario/cliente/lista_clientes.html'
    login_url = reverse_lazy('usuario:iniciar_sesion')
    paginacion = None
    numero_clientes = 3

    def get(self, request):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        Obtiene la lista de todos los clientes que están registrados en el sistema.
        Crea la paginación.
        Se envía al template el namespace de la url EditarProductos, dependiendo del
        usuario que esté realizando la acción (Administrador o Vendedor). Está url
        se utiliza para asignarla a la opción de editar de cada uno de los registros de la tabla.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
                request.user.has_perm(Usuario.PERMISO_VENDEDOR):

            context = {
                'form': BusquedaClienteForm(),
                'namespace_editar_cliente': get_namespace(request, view='editar_cliente')
            }

            page = request.GET.get('page')

            self.paginacion = Paginator(Cliente.objects.all(), self.numero_clientes)

            context['clientes'] = get_objects(self.paginacion, page)
            context['numero_paginas'] = range(1, self.paginacion.num_pages + 1)

            return render(request, self.template_name, context)
        else:
            raise PermissionDenied

    def post(self, request):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        Obtiene un cliente mendiante el formulario de búsqueda, la búsqueda se realiza
        mediante el número de cédula del cliente. Se Valida el formulario y se retorna el resultado.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
                request.user.has_perm(Usuario.PERMISO_VENDEDOR):
            form = BusquedaClienteForm(data=request.POST)

            context = {
                'form': form,
                'namespace_editar_cliente': get_namespace(request, view='editar_cliente')
            }

            if form.is_valid():
                cedula = form.cleaned_data.get('busqueda')
                clientes = Cliente.objects.filter(cedula=cedula)

                context['clientes'] = clientes
                context['resultado'] = len(clientes)

            return render(request, self.template_name, context)
        else:
            raise PermissionDenied


class ActualizacionCliente(LoginRequiredMixin, UpdateView):
    """
    Permite modificar los datos de los clientes.
    """

    model = Cliente
    template_name = 'usuario/cliente/actualizar_cliente.html'
    form_class = ClienteForm
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def get(self, request, *args, **kwargs):
        """
       Verifca el permiso del usuario que está intentado acceder a la vista.
       Si el permiso no es válido deniega el acceso.
       """

        if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
                request.user.has_perm(Usuario.PERMISO_VENDEDOR):

            return super(ActualizacionCliente, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        """
       Verifca el permiso del usuario que está intentado acceder a la vista.
       Si el permiso no es válido deniega el acceso.
       Dependiendo del tipo de usuario que esté realizando la petición, se define la
       url a donde será redirigido una vez se hayan actualizado los datos.
       """

        if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
                request.user.has_perm(Usuario.PERMISO_VENDEDOR):

            if request.session.get('rol') == Usuario.ADMIN:
                self.success_url = reverse_lazy('usuario:admin_listar_clientes')
            elif request.session.get('rol') == Usuario.VENDEDOR:
                self.success_url = reverse_lazy('usuario:vendedor_listar_clientes')

            return super(ActualizacionCliente, self).post(request, *args, **kwargs)
        else:
            raise PermissionDenied


class EliminacionCliente(LoginRequiredMixin, DeleteView):

    """
    Permite al usuario Administrador eliminar a los clientes del sistema.
    """

    model = Cliente
    login_url = reverse_lazy('usuario:iniciar_sesion')
    success_url = reverse_lazy('usuario:admin_listar_clientes')

    def get(self, request, *args, **kwargs):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        """

        if request.user.has_perm(Usuario.ADMIN):
            return super(EliminacionCliente, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        """
       Verifca el permiso del usuario que está intentado acceder a la vista.
       Si el permiso no es válido deniega el acceso.
       """

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
        Procesa la petición HTTP por el método GET.
        Se instancia el formulario de inicio de sesión y se envía
        al template.
        Si ya hay una sesión iniciada entonces se redirige al usuario a su vista correspondiente.
        :param request: Contiene la información de la petición HTTP.
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
        método POST.
        Se instancia el formulario de Inicio de Sesión, para validar los datos.
        Luego se verifica el estado de la cuenta del usuario, su está activa
        Se crea la sesión y se redirecciona a su respectiva vista y de lo contrario
        no se permite el acceso a la aplicación.

        :param request: Contiene la información de la petición HTTP.
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
                    messages.warning(request, u'Esta cuenta no está activa.')
            else:
                messages.error(request, u'El correo y/o la contraseña no coinciden.')

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
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        Obtiene una lista de las cuentas que aún no han sido activadas.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN):

            usuarios_inactivos = Usuario.objects.filter(activo=False)

            context = {'usuarios': usuarios_inactivos}

            return render(request, self.template_name, context)
        else:
            raise PermissionDenied

    def post(self, request):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        Recibe los datos del formulario de activación y los valída. Luego activa las cuentas
        e informa al usuario vendedor por medio de un mensaje de correo electrónico.
        """

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


class ListaVendedor(LoginRequiredMixin, View):
    """
    Mustra la lista de los usuarios vendedores.
    """
    template_name = 'usuario/admin/listar_vendedores.html'
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def get(self, request):
        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            context = {
                'vendedores': Usuario.objects.filter(rol=Usuario.VENDEDOR)
            }
            return render(request, self.template_name, context)
        else:
            raise PermissionDenied


class EliminacionCuenta(LoginRequiredMixin, View):

    """
    Permite al usuario administrador eliminar las cuentas de los usuarios vendedores.
    """

    login_url = reverse_lazy('usuario:iniciar_sesion')
    success_url = reverse_lazy('usuario:listar_vendedores')

    def get(request):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        """
        if request.user.has_perm(Usuario.ADMIN):
            raise Http404
        else:
            raise PermissionDenied

    def post(self, request, **kwargs):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el
        """
        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            pk = kwargs.get('pk')
            user = get_object_or_404(User, pk=pk)
            usuario = get_object_or_404(Usuario, user=user)

            if usuario.rol == 'vendedor':
                user.delete()
                return HttpResponseRedirect(self.success_url)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied


class HomeAdmin(LoginRequiredMixin, View):
    """
    Muestra la vista del home del administrador.
    """

    template_name = 'usuario/admin/home.html'
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def get(self, request):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        """

        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            cuentas_sin_activar = Usuario.objects.filter(activo=False)

            return render(request, self.template_name, {'numero_cuentas': len(cuentas_sin_activar)})
        else:
            raise PermissionDenied


class HomeVendedor(LoginRequiredMixin, View):
    """
    Muestra la vista del Home Vendedor.
    """
    template_name = 'usuario/vendedor/home.html'
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def get(self, request):
        """
        Verifca el permiso del usuario que está intentado acceder a la vista.
        Si el permiso no es válido deniega el acceso.
        """

        if request.user.has_perm(Usuario.PERMISO_VENDEDOR):
            return render(request, self.template_name, {})
        else:
            raise PermissionDenied


@login_required(login_url=reverse_lazy('usuario:iniciar_sesion'))
def cerrar_sesion(request):
    """
    Verifca el permiso del usuario que está intentado acceder a la vista.
    Si el permiso no es válido deniega el acceso.
    Cierra la sesión actual y redirecciona al usuario a la vista de inicio de sesión.
    """

    if request.user.has_perm(Usuario.PERMISO_ADMIN) or \
            request.user.has_perm(Usuario.PERMISO_VENDEDOR):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('usuario:iniciar_sesion'))
    else:
        raise PermissionDenied


@login_required(login_url=reverse_lazy('usuario:iniciar_sesion'))
def buscar_cliente(request):
    if request.user.has_perm(Usuario.PERMISO_VENDEDOR):
        if request.method == 'POST':
            datos = json.loads(request.body)
            form = FormBusquedaCliente(data=datos)

            if form.is_valid():
                cedula = form.cleaned_data.get('cedula')

                try:
                    cliente = Cliente.objects.get(cedula=cedula)
                except ObjectDoesNotExist:
                    cliente = None

                if cliente:
                    response = {
                        "response": "success",
                        "id": cliente.id,
                        "cedula": cliente.cedula,
                        "nombre": cliente.nombre_completo(),
                        "direccion": cliente.direccion,
                        "telefono": cliente.telefono,
                        "ciudad": cliente.ciudad.get_nombre()
                    }
                else:
                    response = {
                        "response": "empty",
                        "mensaje": u"El cliente no existe."
                    }
            else:
                print form.errors
                response = {
                    "response": "error-form",
                    "mensaje": form.errors['cedula'][0]
                }

            return HttpResponse(json.dumps(response))
    else:
        raise PermissionDenied


def registrar_cliente(request):
    if request.user.has_perm(Usuario.PERMISO_VENDEDOR):
        data = json.loads(request.body)
        form = ClienteForm(data=data)

        if form.is_valid():
            cliente = form.save()
            response = {
                'response': 'success',
                'id': cliente.id,
                'cedula': cliente.cedula,
                'nombre': cliente.nombre_completo(),
                'ciudad': cliente.ciudad.get_nombre(),
                'telefono': cliente.telefono,
                'direccion': cliente.direccion
            }
        else:
            response = {'response': 'error', 'errors': form.errors}

        return HttpResponse(json.dumps(response))
    else:
        raise PermissionDenied
