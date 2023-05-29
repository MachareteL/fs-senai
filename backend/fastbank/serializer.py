from rest_framework import serializers
from .models import *

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['tipo_conta', 'cliente', 'numero_conta', 'agencia', 'digito', 'saldo', 'data_criacao', 'conta_ativa']

class CartaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartao
        fields = ['numero_cartao', 'conta', 'cvv', 'data_vencimento', 'nome_titular_cartao', 'bandeira', 'cartao_ativo']

class MovimentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimentacao
        fields = ['conta', 'cartao', 'data_hora', 'operacao', 'valor', 'destinatario'] 

class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprestimo
        fields = ['conta', 'data_solicitacao', 'valor_solicitado', 'juros', 'aprovado', 'numero_parcela', 'data_aprovacao', 'observacao']

class InvestimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investimento
        fields = ['conta', 'aporte', 'rentabilidade', 'finalizado']

class ContatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contatos
        fields = ['cliente', 'numero_telefone', 'email', 'observacao']

class EnderecoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'