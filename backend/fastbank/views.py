from django.shortcuts import get_object_or_404, render
from .serializer import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import get_user_model
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from django.http import Http404
from .models import Conta as ContaModel, Cliente as ClienteModel
from .models import Movimentacao as MovimentacaoModel
from decimal import Decimal

def getUserId(request):
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    acess = AccessToken(token)
    usuario = acess['user_id']
    return usuario 


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

    def create(self, request, *args, **kwargs):
        usuario = getUserId(request)
        cliente = ClienteModel.objects.get(id=usuario)
        req = request.data
        variavel = Endereco.objects.create(rua=req['rua'], numero=req['numero'], bairro=req['bairro'] ,cidade= req['cidade'], cliente=cliente, UF= req['uf'], cep=req['cep'])
        inst = Endereco.objects.filter(cep=variavel)
        res = EnderecoClienteSerializer(inst, many=True)
        return Response(res.data)
    
    def list(self, request, *args, **kwargs):
        usuario = getUserId(request)
        cliente = ClienteModel.objects.get(id=usuario)
        endereco = Endereco.objects.filter(cliente=cliente)
        retorno = EnderecoClienteSerializer(endereco, many=True)
        return Response(retorno.data)

class Movimentacao(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all().order_by('-data_hora')
    serializer_class = MovimentacaoSerializer

    def create(self, request, *args, **kwargs):
        req = request.data #{'conta' 'cartao' 'operacao' 'valor'}
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        acess = AccessToken(token)
        usuario = acess['user_id']
        valor = req['valor']
        if Decimal(valor) <= 0:
            raise PermissionDenied("O valor não deve ser menor ou igual a 0")

        if req['operacao'] == 'DP' or req['operacao'] == "ET":
            destino = ContaModel.objects.get(cliente=usuario)
            destino.saldo += Decimal(valor)
            destino.save()

        if req['operacao'] == 'PX' or req['operacao'] == 'TC':
            destino = req['destinatario']
            print('o valor é '+ valor)
            print('o destino '+ destino)

            try:
                user_pix = ClienteModel.objects.get(cpf_cnpj= destino)
                conta_destinataria = ContaModel.objects.get(cliente=user_pix)
            except:
                print('Error')
                raise NotFound("Esse CPF não existe ou não está cadastrado como uma chave PIX")

            conta_rementente = ContaModel.objects.get(cliente=usuario)
            if conta_rementente.saldo >= Decimal(valor):
                conta_destinataria.saldo += Decimal(valor)
                conta_rementente.saldo -= Decimal(valor)
                conta_destinataria.save()
                conta_rementente.save()
            else:
                raise PermissionDenied("Saldo insuficiente")
        
            
        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        req = request.data #{'conta' 'cartao' 'operacao' 'valor'}
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        acess = AccessToken(token)
        usuario = acess['user_id']
        instancia = MovimentacaoModel.objects.filter(conta=usuario).order_by('-data_hora')
        print(instancia)
        res = MovimentacaoSerializer(instancia, many=True)
        return Response(res.data)

class Cliente(viewsets.ReadOnlyModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class FAQ(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer