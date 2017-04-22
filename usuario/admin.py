from django.contrib import admin
from .models import (
    Ciudad,
    Cliente,
    Departamento,
    Usuario
)


class ClienteAdmin(admin.ModelAdmin):

    list_display = ['cedula', 'nombres', 'apellidos', 'ciudad', 'telefono', 'direccion']

    class Meta:
        model = Cliente


class UsuarioAdmin(admin.ModelAdmin):

    list_display = ['user', 'nombres', 'apellidos', 'rol', 'activo']

    class Meta:
        model = Usuario


admin.site.register(Ciudad)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Departamento)
admin.site.register(Usuario, UsuarioAdmin)
