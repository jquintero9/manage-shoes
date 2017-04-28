#!usr/local/bin
# coding: latin-1

from django import forms
from django.core.validators import RegexValidator
from usuario.utils import regex, error_messages
from .models import Producto


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
