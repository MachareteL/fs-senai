from django.shortcuts import render
from .serializer import *
from rest_framework import viewsets


class Cliente(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class Conta(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer

class Cartao(viewsets.ModelViewSet):
    queryset = Cartao.objects.all()
    serializer_class = CartaoSerializer

class TipoCliente(viewsets.ModelViewSet):
    queryset = TipoCliente.objects.all()
    serializer_class = TipoClienteSerializer

class EnderecoCliente(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoClienteSerializer
# Create your views here.
