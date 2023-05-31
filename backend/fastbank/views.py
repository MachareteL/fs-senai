from django.shortcuts import get_object_or_404, render
from .serializer import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import get_user_model
from rest_framework.response import Response
from .models import Conta as ContaModel
from .models import Movimentacao as MovimentacaoModel
from decimal import Decimal

class Conta(viewsets.ReadOnlyModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    # permission_classes = (IsAuthenticated, )
    def list(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        # print(token)
        dados = AccessToken(token)
        # print(dados)
        usuario = dados['user_id']
        print(usuario)    
        # responsavel = get_object_or_404(Cliente, id=usuario)
        contaResponsavel = ContaModel.objects.get(cliente=usuario)
        serializer = ContaSerializer(contaResponsavel)
        return Response(data=serializer.data, status=200)

class Cartao(viewsets.ModelViewSet):
    queryset = Cartao.objects.all()
    serializer_class = CartaoSerializer

class EnderecoCliente(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoClienteSerializer

class Movimentacao(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all().order_by('-data_hora')
    serializer_class = MovimentacaoSerializer

    def create(self, request, *args, **kwargs):
        req = request.data #{'conta' 'cartao' 'operacao' 'valor'}
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        acess = AccessToken(token)
        usuario = acess['user_id']

        if req['operacao'] == 'DP':
            destino = ContaModel.objects.get(cliente=usuario)
            valor = req['valor']
            destino.saldo += Decimal(valor)
            destino.save()
        return super().create(request, *args, **kwargs)
    
    # def list(self, request, *args, **kwargs):
    #     req = request.data #{'conta' 'cartao' 'operacao' 'valor'}
    #     token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    #     acess = AccessToken(token)
    #     usuario = acess['user_id']
    #     instancia = MovimentacaoModel.objects.filter(conta=usuario).order_by('-data_hora')
    #     print(instancia)
    #     res = MovimentacaoSerializer(instancia, many=True)
    #     return Response(res.data)
    
class Cliente(viewsets.ReadOnlyModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer