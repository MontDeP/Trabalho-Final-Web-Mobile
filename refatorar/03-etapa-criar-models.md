# Etapa 03 — Criar os Models

## Objetivo

Criar os Models do seu domínio, replicando os padrões usados pelo professor em `veiculo/models.py` e `anuncio/models.py`.

## Status

- [ ] Concluído

## Referência: O que o professor fez

### `veiculo/models.py` (referência)

```python
from datetime import datetime
from django.db import models
from .consts import OPCOES_MARCAS, OPCOES_CORES, OPCOES_COMBUSTIVEIS

class Veiculo(models.Model):
    marca       = models.SmallIntegerField(choices=OPCOES_MARCAS)
    modelo      = models.CharField(max_length=100)
    ano         = models.IntegerField()
    cor         = models.SmallIntegerField(choices=OPCOES_CORES)
    combustivel = models.SmallIntegerField(choices=OPCOES_COMBUSTIVEIS)
    foto        = models.ImageField(upload_to='veiculo/fotos', null=True, blank=True)
    criado_em   = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.get_marca_display()} {self.modelo}'

    @property
    def veiculo_novo(self):
        return self.ano == datetime.now().year

    def anos_de_uso(self):
        return datetime.now().year - self.ano
```

### `anuncio/models.py` (referência)

```python
from django.db import models
from django.contrib.auth.models import User
from veiculo.models import Veiculo

class Anuncio(models.Model):
    titulo      = models.CharField(max_length=100)
    descricao   = models.TextField()
    veiculo     = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    usuario     = models.ForeignKey(User, on_delete=models.CASCADE)
    preco       = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em   = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
```

## O que fazer

### 1. Criar o Model da Entidade Principal

Arquivo: `python/sistema/ENTIDADE_PRINCIPAL/models.py`

Siga este template, adaptando para o seu domínio:

```python
from datetime import datetime
from django.db import models
# Se tiver choices:
# from .consts import OPCOES_CATEGORIA, OPCOES_TIPO

class EntidadePrincipal(models.Model):
    # CAMPOS OBRIGATÓRIOS (adaptar para o seu domínio)
    # campo1 = models.CharField(max_length=100)
    # campo2 = models.IntegerField()
    # campo3 = models.SmallIntegerField(choices=OPCOES_CATEGORIA)
    # foto   = models.ImageField(upload_to='entidade/fotos', null=True, blank=True)
    
    # CAMPOS DE AUDITORIA (manter igual ao professor)
    criado_em     = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.campo1}'  # adaptar

    # Adicione propriedades calculadas relevantes para seu domínio
    # @property
    # def alguma_propriedade(self):
    #     return ...
```

### 2. Criar o Model da Entidade Secundária

Arquivo: `python/sistema/ENTIDADE_SECUNDARIA/models.py`

```python
from django.db import models
from django.contrib.auth.models import User
from ENTIDADE_PRINCIPAL.models import EntidadePrincipal

class EntidadeSecundaria(models.Model):
    titulo           = models.CharField(max_length=100)
    descricao        = models.TextField()
    entidade_principal = models.ForeignKey(EntidadePrincipal, on_delete=models.CASCADE)
    usuario          = models.ForeignKey(User, on_delete=models.CASCADE)
    # outros campos do seu domínio
    # preco = models.DecimalField(max_digits=10, decimal_places=2)
    
    criado_em        = models.DateTimeField(auto_now_add=True)
    atualizado_em    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
```

### 3. Registrar no admin.py de cada app

Arquivo: `python/sistema/ENTIDADE_PRINCIPAL/admin.py`

```python
from django.contrib import admin
from .models import EntidadePrincipal

@admin.register(EntidadePrincipal)
class EntidadePrincipalAdmin(admin.ModelAdmin):
    list_display = ['campo1', 'campo2', 'criado_em']  # adaptar
```

Arquivo: `python/sistema/ENTIDADE_SECUNDARIA/admin.py`

```python
from django.contrib import admin
from .models import EntidadeSecundaria

@admin.register(EntidadeSecundaria)
class EntidadeSecundariaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'criado_em']
```

### 4. Criar e aplicar as migrações

```bash
cd python/sistema

python manage.py makemigrations ENTIDADE_PRINCIPAL
python manage.py makemigrations ENTIDADE_SECUNDARIA
python manage.py migrate
```

### 5. Testar no Admin

```bash
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/admin/` e verifique se os modelos aparecem.

## Padrões obrigatórios (não improvise)

| Padrão | Por quê |
|--------|---------|
| `auto_now_add=True` em `criado_em` | Auditoria automática |
| `auto_now=True` em `atualizado_em` | Auditoria automática |
| `on_delete=models.CASCADE` nas FK | Consistência — o professor usou isso |
| `FK → User` na entidade secundária | O anúncio pertence a um usuário |
| `__str__` implementado | Admin e displays funcionam corretamente |

## O que NÃO fazer nesta etapa

- Não crie Views ainda
- Não crie Forms ainda
- Não mexa nos Templates ainda

## Verificação

```bash
python manage.py check
python manage.py showmigrations
```

## Próxima Etapa

[Etapa 04 — Criar os Forms e Views](04-etapa-criar-views-e-forms.md)
