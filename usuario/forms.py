#!usr/local/bin
# coding: latin-1

from django import forms
from .models import Usuario
from django.core.validators import EmailValidator, RegexValidator
from .utils import regex, error_messages


class UserForm(forms.Form):

    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                'max_length': '150',
                'class': 'validate',
            }
        ),
        validators=[
            EmailValidator()
        ],
        error_messages={
            'required': u'¿Cúal es tu correo electrónico?'
        }
    )

    password = forms.CharField(
        max_length=16,
        widget=forms.PasswordInput(
            attrs={
                'class': 'validate',
            }
        ),
        validators=[
            RegexValidator(regex=regex['password'], message=error_messages['password'])
        ]
    )

    confirmar_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'validate',
            }
        )
    )

    def clean_confirmar_password(self):
        password = self.cleaned_data.get('password')
        confirmar_password = self.cleaned_data.get('confirmar_password')

        if not (password == confirmar_password):
            raise forms.ValidationError(u'Las contraseñas no coinciden.')

        return confirmar_password


class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'rol']

        widgets = {
            'nombres': forms.TextInput(
                attrs={
                    'class': 'validate',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'validate',
                }
            )
        }


class LoginForm(forms.Form):

    email = forms.CharField(
        max_length=150,
        widget=forms.EmailInput(
            attrs={
                'class': 'validator'
            }
        ),
        validators=[
            EmailValidator()
        ],
        error_messages={
            'required': u'¿Cúal es tu correo electrónico?'
        }
    )

    password = forms.CharField(
        max_length=16,
        widget=forms.PasswordInput()
    )
