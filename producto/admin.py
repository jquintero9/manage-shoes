from django.contrib import admin
from .models import (
    Marca,
    Producto,
    Factura,
    DetalleFactura,
    Talla,
)

# Register your models here.


class ProductoAdmin(admin.ModelAdmin):

    list_display = ['id_referencia', 'marca', 'nombre', 'stock', 'precio']

    class Meta:
        model = Producto


class FacturaAdmin(admin.ModelAdmin):

    list_display = ['id', 'cliente', 'fecha', 'total_pagar']

    class Meta:
        model = Factura


class DetalleFacturaAdmin(admin.ModelAdmin):

    list_display = ['id', 'factura', 'producto', 'cantidad', 'total']

    class Meta:
        model = DetalleFactura


admin.site.register(Marca)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(DetalleFactura, DetalleFacturaAdmin)
admin.site.register(Talla)

