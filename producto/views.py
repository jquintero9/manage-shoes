from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .models import Producto
from usuario.models import Usuario
from .forms import ProductoForm

# Create your views here.


class CreacionProducto(LoginRequiredMixin, CreateView):

    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear_producto.html'
    success_url = reverse_lazy('usuario:admin_home')
    login_url = reverse_lazy('usuario:iniciar_sesion')

    def get(self, request, *args, **kwargs):
        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(CreacionProducto, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        if request.user.has_perm(Usuario.PERMISO_ADMIN):
            return super(CreacionProducto, self).post(request, *args, **kwargs)

