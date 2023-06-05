from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
rota = DefaultRouter()

# rota.register('cliente', viewset=ClienteView)
rota.register('cartao', viewset=Cartao)
rota.register('conta', viewset=Conta)
rota.register('enderecoCliente', viewset=EnderecoCliente)
rota.register('movimentacao', viewset=Movimentacao)
rota.register('cliente', viewset=Cliente)
rota.register('FAQ', viewset=FAQ)
urlpatterns = []+rota.urls