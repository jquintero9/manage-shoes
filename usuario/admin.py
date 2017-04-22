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


admin.site.register(Ciudad)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Departamento)
admin.site.register(Usuario)
