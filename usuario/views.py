#!usr/local/bin
# coding: latin-1

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserForm, UsuarioForm, LoginForm
from .models import Usuario


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
        la instancia del modelo Usuario.
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


class InicioSesion(View):

    """
    Auntentica los usuairos de tipo Administrador y Vendedor.
    """

    template_name = 'usuario/autenticacion/iniciar_sesion.html'
    form_class = None

    def get(self, request):

        """
        Procesa la petición HTTP por el método GET.
        Se instancia el formulario de inicio de sesión y se envía
        al template.
        :param request: Contiene la información de la petición HTTP.
        :return: La vista Registrar Vendedor.
        """

        self.form_class = LoginForm()
        context = {'form': self.form_class}

        return render(request, self.template_name, context)

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
                    url_admin = reverse_lazy('usuario:admin_home')
                    url_vendedor = reverse_lazy('usuario:vendedor_home')
                    url_redirect = url_admin if usuario.rol == Usuario.ADMIN else url_vendedor

                    return HttpResponseRedirect(url_redirect)
                else:
                    messages.warning(request, u'Esta cuenta no está activa.')
            else:
                messages.error(request, u'El correo y/o la contraseña no coinciden.')

        context = {'form': self.form_class}

        return render(request, self.template_name, context)


def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('usuario:iniciar_sesion'))

