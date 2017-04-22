from django.conf.urls import url
from .views import (
    RegistroVendedor,
)

urlpatterns = [
    url(r'^registrar$', RegistroVendedor.as_view(), name='registrar_vendedor'),
]