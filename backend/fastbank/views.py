from django.shortcuts import get_object_or_404, render
from .serializer import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import get_user_model
from rest_framework.response import Response
from .models import Conta as ContaModel
import json

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
        responsavel = Cliente.objects.get(id=usuario)
        # responsavel = get_object_or_404(Cliente, id=usuario)
        print(responsavel)
        contaResponsavel = ContaModel.objects.get(cliente=responsavel)
        serializer = ContaSerializer(contaResponsavel)
        return Response(data=serializer.data, status=200)

class Cartao(viewsets.ModelViewSet):
    queryset = Cartao.objects.all()
    serializer_class = CartaoSerializer

class EnderecoCliente(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoClienteSerializer
