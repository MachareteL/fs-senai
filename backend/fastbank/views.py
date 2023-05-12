from django.shortcuts import render
from .serializer import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
import json

class ClienteView(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class Conta(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    # permission_classes = (IsAuthenticated, )
    def list(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        # print(token)
        dados = AccessToken(token)
        usuario = dados['user_id']
        print(usuario)
        responsavel = Cliente.objects.filter(id=usuario)
        print(responsavel)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # objeto = json.loads((request.body).decode('utf-8'))
        # print(objeto['nome_cliente_conta'])
        return super().create(request, *args, **kwargs)

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
