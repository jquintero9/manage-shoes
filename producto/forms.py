#!usr/local/bin
# coding: latin-1

from django import forms
from django.core.validators import RegexValidator
from usuario.utils import regex, error_messages
from .models import Producto, Marca


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

