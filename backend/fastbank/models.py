from django.db import models

# Create your models here.
class Clientes(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14)
    data_cadastro = models.DateField(auto_now=True)
    foto = models.ImageField()