from django.shortcuts import render
from django.views.generic import View
from .forms import UserForm, UsuarioForm


class RegistroVendedor(View):

    template_name = 'usuario/autenticacion/registrar_vendedor.html'
    user_form = usuario_form = None

    def get(self, request):

        self.user_form = UserForm()
        self.usuario_form = UsuarioForm()

        context = {
            'user_form': self.user_form,
            'usuario_form': self.usuario_form
        }

        return render(request, self.template_name, context)


