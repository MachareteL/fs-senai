# Generated by Django 4.2.1 on 2023-05-23 19:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('nome_cliente', models.CharField(max_length=100)),
                ('tipo_cliente', models.CharField(choices=[('F', 'Pessoa Física'), ('J', 'Pessoa Jurídica')], default='F', max_length=1)),
                ('foto', models.ImageField(upload_to='imagens/')),
                ('cpf_cnpj', models.CharField(max_length=20, unique=True)),
                ('data_nascimento', models.DateField()),
                ('data_criacao', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Cartao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_cartao', models.CharField(max_length=20)),
                ('cvv', models.IntegerField()),
                ('data_vencimento', models.DateField()),
                ('nome_titular_cartao', models.CharField(max_length=100)),
                ('bandeira', models.CharField(choices=[('M', 'Bandeira Visa'), ('V', 'Bandeira MasterCard')], default='V', max_length=2)),
                ('cartao_ativo', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Cartões',
            },
        ),
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_conta', models.CharField(choices=[('CC', 'Conta Corrente'), ('CP', 'Conta Poupança')], default='CC', max_length=2)),
                ('numero_conta', models.IntegerField()),
                ('agencia', models.IntegerField()),
                ('digito', models.IntegerField()),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_criacao', models.DateField(auto_now=True)),
                ('conta_ativa', models.BooleanField(default=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Contas',
            },
        ),
        migrations.CreateModel(
            name='Movimentacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField(auto_now=True)),
                ('operacao', models.CharField(choices=[('TD', 'Transferência Débito'), ('TC', 'Transferência Crédito'), ('DP', 'Transferência Crédito'), ('PX', 'Transferência PIX')], default='TD', max_length=2)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cartao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='fastbank.cartao')),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fastbank.conta')),
            ],
        ),
        migrations.CreateModel(
            name='Investimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aporte', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rentabilidade', models.DecimalField(decimal_places=2, max_digits=10)),
                ('finalizado', models.BooleanField()),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fastbank.conta')),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rua', models.CharField(max_length=100)),
                ('numero', models.IntegerField()),
                ('bairro', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('UF', models.CharField(max_length=2)),
                ('complemento', models.CharField(blank=True, max_length=100, null=True)),
                ('cep', models.CharField(max_length=8)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Endereços',
            },
        ),
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_solicitacao', models.DateField()),
                ('valor_solicitado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('juros', models.DecimalField(decimal_places=2, max_digits=10)),
                ('aprovado', models.BooleanField()),
                ('numero_parcela', models.IntegerField()),
                ('data_aprovacao', models.DateField()),
                ('observacao', models.TextField()),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fastbank.conta')),
            ],
        ),
        migrations.CreateModel(
            name='Contatos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_telefone', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('observacao', models.CharField(max_length=255)),
                ('codigo_cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Contatos',
            },
        ),
        migrations.CreateModel(
            name='ClienteConta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fastbank.conta')),
            ],
        ),
        migrations.AddField(
            model_name='cartao',
            name='conta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fastbank.conta'),
        ),
        migrations.AddConstraint(
            model_name='cartao',
            constraint=models.UniqueConstraint(fields=('numero_cartao',), name='unique_numero_cartao'),
        ),
    ]
