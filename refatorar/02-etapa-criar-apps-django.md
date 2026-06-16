# Etapa 02 — Criar os Novos Apps Django

## Objetivo

Substituir os apps `veiculo` e `anuncio` pelos apps do seu domínio. O sistema do professor tem dois apps com relacionamento de Foreign Key. Você deve criar dois apps equivalentes no seu tema.

## Status

- [ ] Concluído

## Estrutura a Replicar

O professor criou:
- App `veiculo` → entidade principal (o "produto" do seu marketplace)
- App `anuncio` → entidade secundária que referencia a principal (o "anúncio" do produto)

Você vai criar:
- App `ENTIDADE_PRINCIPAL` → substitui `veiculo`
- App `ENTIDADE_SECUNDARIA` → substitui `anuncio`

> Exemplo: se o tema for **biblioteca**, seria `livro` e `emprestimo`
> Exemplo: se o tema for **imóveis**, seria `imovel` e `anuncio`

## O que fazer

### 1. Criar os novos apps

```bash
cd python/sistema

python manage.py startapp ENTIDADE_PRINCIPAL
python manage.py startapp ENTIDADE_SECUNDARIA
```

Isso cria a estrutura:
```
ENTIDADE_PRINCIPAL/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── views.py
└── migrations/
    └── __init__.py
```

### 2. Registrar os apps em `settings.py`

Arquivo: `python/sistema/sistema/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # apps do professor (remover depois)
    # 'veiculo.apps.VeiculoConfig',
    # 'anuncio.apps.AnuncioConfig',
    # seus novos apps
    'ENTIDADE_PRINCIPAL.apps.EntidadePrincipalConfig',
    'ENTIDADE_SECUNDARIA.apps.EntidadeSecundariaConfig',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken'
]
```

> **ATENÇÃO**: Não remova os apps do professor ainda. Remova apenas quando seus apps estiverem funcionando.

### 3. Criar o arquivo `consts.py` (se necessário)

Se o seu domínio tiver choices/opções fixas (como marcas, categorias, tipos), crie:

Arquivo: `python/sistema/ENTIDADE_PRINCIPAL/consts.py`

Siga o mesmo padrão de `veiculo/consts.py`:
```python
OPCOES_CATEGORIA = [
    (1, 'CATEGORIA_1'),
    (2, 'CATEGORIA_2'),
    (3, 'CATEGORIA_3'),
]

OPCOES_TIPO = [
    (1, 'TIPO_1'),
    (2, 'TIPO_2'),
]
```

### 4. Criar o `urls.py` de cada app

O Django não cria o `urls.py` automaticamente. Crie manualmente:

Arquivo: `python/sistema/ENTIDADE_PRINCIPAL/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    # será preenchido na etapa de Views
]
```

Arquivo: `python/sistema/ENTIDADE_SECUNDARIA/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    # será preenchido na etapa de Views
]
```

### 5. Criar o `serializers.py` de cada app

Arquivo: `python/sistema/ENTIDADE_PRINCIPAL/serializers.py`
```python
# será preenchido na etapa de API REST
```

Arquivo: `python/sistema/ENTIDADE_SECUNDARIA/serializers.py`
```python
# será preenchido na etapa de API REST
```

### 6. Criar o `forms.py` de cada app

Arquivo: `python/sistema/ENTIDADE_PRINCIPAL/forms.py`
```python
# será preenchido na etapa de Views
```

## O que NÃO fazer nesta etapa

- Não crie os Models ainda (próxima etapa)
- Não remova os apps do professor ainda
- Não crie Views ainda

## Verificação

```bash
python manage.py check
```

Deve retornar `System check identified no issues`.

## Próxima Etapa

[Etapa 03 — Criar os Models](03-etapa-criar-models.md)
