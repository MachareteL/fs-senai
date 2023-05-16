from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import *
rota = DefaultRouter()

rota.register('cliente', viewset=ClienteView)
rota.register('cartao', viewset=Cartao)
rota.register('conta', viewset=Conta)
rota.register('enderecoCliente', viewset=EnderecoCliente)

urlpatterns = []+rota.urls