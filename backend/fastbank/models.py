from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    UF = models.CharField(max_length=2)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=8)
    def __str__(self) -> str:
        return self.cep 
    class Meta:
        verbose_name_plural = "Endereço"


class TipoCliente(models.Model):
    PESSOA_FISICA = "F"
    PESSOA_JURIDICA = "J"

    TIPO_CLIENTE = [
        (PESSOA_FISICA, "Pessoa Física"),
        (PESSOA_JURIDICA, "Pessoa Jurídica"),
    ]

    tipo_cliente = models.CharField(
        max_length=1, choices=TIPO_CLIENTE, default=PESSOA_FISICA
    )
    def __str__(self) -> str:
        return self.tipo_cliente


class CustomUserManager(BaseUserManager):
    def create_user(self, cpf_cnpj, password=None, **extra_fields):
        """
        Cria e salva um usuário com o CPF e senha fornecidos.
        """
        if not cpf_cnpj:
            raise ValueError('O CPF é obrigatório')
        
        user = self.model(cpf_cnpj=cpf_cnpj, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, cpf, password=None, **extra_fields):
        """
        Cria e salva um superusuário com o CPF e senha fornecidos.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cpf, password, **extra_fields)

    

class Cliente(AbstractBaseUser):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    username = None

    USERNAME_FIELD = 'cpf_cnpj'
    REQUIRED_FIELDS = ['nome_cliente', 'endereco_cliente', 'tipo_cliente', 'foto', 'data_nascimento', ]

    def __str__(self):
        return self.cpf


    nome_cliente = models.CharField(max_length=100)
    endereco_cliente = models.ForeignKey(Endereco, on_delete=models.PROTECT)
    tipo_cliente = models.ForeignKey(TipoCliente, on_delete=models.DO_NOTHING)
    foto = models.ImageField(upload_to="imagens/")
    cpf_cnpj = models.CharField(max_length=20, unique=True)
    data_nascimento = models.DateField()
    data_criacao = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.nome_cliente

    class Meta:
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=["usuario"],
        #         name="unique_cliente_user",
        #     )
        # ]
        verbose_name_plural = "Clientes"
    





class Contatos(models.Model):
    codigo_cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    numero_telefone = models.IntegerField()
    email = models.EmailField()
    observacao = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Contatos"


class Conta(models.Model):
    CONTA_CORRENTE = "CC"
    CONTA_POUPANCA = "CP"

    TIPO_CONTA = [
        (CONTA_CORRENTE, "Conta Corrente"),
        (CONTA_POUPANCA, "Conta Poupança"),
    ]

    tipo_conta = models.CharField(
        max_length=2, choices=TIPO_CONTA, default=CONTA_CORRENTE
    )
    nome_cliente_conta = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    numero_conta = models.IntegerField()
    agencia = models.IntegerField()
    digito = models.IntegerField()
    saldo = models.IntegerField()
    data_criacao = models.DateField(auto_now=True)
    conta_ativa = models.BooleanField()

    class Meta:
        verbose_name_plural = "Conta"

    def __str__(self) -> str:
        return self.numero_conta


class Cartao(models.Model):
    numero_cartao = models.CharField(max_length=20)
    conta_cartao = models.ForeignKey(Conta, on_delete=models.DO_NOTHING)
    cvv = models.IntegerField()
    data_vencimento = models.DateField()
    bandeira = models.CharField(max_length=20)
    nome_titular_cartao = models.CharField(max_length=100)
    cartao_ativo = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["numero_cartao"],
                name="unique_numero_cartao",
            )
        ]
        verbose_name_plural = "Cartao"


class Movimentacao(models.Model):
    DEBITO = "D"
    CREDITO = "C"
    PIX = "P"


    TIPO_OPERACAO = [
        (DEBITO, "Transferência Débito"),
        (CREDITO, "Transferência Crédito"),
        (PIX, "Transferência PIX"),
    ]

    codigo_cartao = models.ForeignKey(Cartao, on_delete=models.PROTECT)
    data_hora = models.DateTimeField(auto_now=True)
    operacao = models.CharField(max_length=1, choices=TIPO_OPERACAO, default=DEBITO)
    valor = models.DecimalField(max_digits=10, decimal_places=2)


class Emprestimo(models.Model):
    codigo_conta = models.ForeignKey(Conta, on_delete=models.DO_NOTHING)
    data_solicitacao = models.DateField()
    valor_solicitado = models.DecimalField(max_digits=10, decimal_places=2)
    juros = models.DecimalField(max_digits=10, decimal_places=2)
    aprovado = models.BooleanField()
    numero_parcela = models.IntegerField()
    data_aprovacao = models.DateField()
    observacao = models.TextField()


class Investimento(models.Model):
    codigo_conta = models.ForeignKey(Conta, on_delete=models.DO_NOTHING)
    aporte = models.DecimalField(max_digits=10, decimal_places=2)
    rentabilidade = models.DecimalField(max_digits=10, decimal_places=2)
    finalizado = models.BooleanField()


class ClienteConta(models.Model):
    codigo_conta = models.ForeignKey(Conta, on_delete=models.DO_NOTHING)
    codigo_cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
