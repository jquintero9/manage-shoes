from django import forms
from .models import Usuario
from django.core.validators import EmailValidator, RegexValidator
from .utils import regex, error_messages


class UserForm(forms.Form):

    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                'max_length': '254',
                'class': 'validate',
            }
        ),
        validators=[
            EmailValidator()
        ]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'max_length': '16',
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


class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos']

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
