#!usr/local/bin
# coding: latin-1

from django import forms
from django.core.validators import RegexValidator
from usuario.utils import regex, error_messages
from .models import Producto, Marca, DetalleFactura, Factura


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = '__all__'


class BusquedaForm(forms.Form):

    busqueda = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'type': 'search', 'placeholder': 'Buscar producto por ID'}),
        validators=[
            RegexValidator(regex=regex['id_referencia'], message=error_messages['id_referencia'])
        ]
    )


class FiltroProductoForm(forms.Form):

    marca = forms.CharField(
        widget=forms.Select(choices=Marca.get_choices()),
        validators=[
            RegexValidator(regex=regex['numero'], message=error_messages['numero'])
        ],
        required=False
    )

    genero = forms.CharField(
        widget=forms.Select(choices=Producto.GENERO),
        validators=[
            RegexValidator(regex=regex['genero'], message=error_messages['genero'])
        ],
        required=False
    )

    estilo = forms.CharField(
        widget=forms.Select(choices=Producto.ESTILO),
        validators=[
            RegexValidator(regex=regex['estilo'], message=error_messages['estilo'])
        ],
        required=False
    )


class BusquedaProductoForm(forms.Form):

    referencia = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese el ID del producto'}),
        validators=[
            RegexValidator(regex=regex['id_referencia'], message=error_messages['id_referencia'])
        ]
    )


class AgregarProductoForm(forms.Form):

    cantidad = forms.IntegerField(
        min_value=1,
        max_value=999,
        error_messages={'required': u'¿Cuantos productos se van a comprar?'}
    )
    referencia = forms.CharField(
        max_length=6,
        widget=forms.TextInput(),
        validators=[
            RegexValidator(regex=regex['id_referencia'], message=error_messages['id_referencia'])
        ]
    )


class FacturaForm(forms.ModelForm):

    class Meta:
        model = Factura
        fields = ['cliente', 'vendedor']


class DetalleFacturaForm(forms.ModelForm):

    class Meta:
        model = DetalleFactura
        fields = ['producto', 'cantidad', 'factura']



