# Etapa 06 — Criar a API REST com DRF

## Objetivo

Criar os Serializers do Django REST Framework para expor os dados das entidades como JSON, para que o app mobile consiga consumir.

## Status

- [ ] Concluído

## Referência: O que o professor fez

### `veiculo/serializers.py` (referência)

```python
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Veiculo

class SerializadorVeiculo(ModelSerializer):
    nome_marca      = SerializerMethodField()
    nome_cor        = SerializerMethodField()
    nome_combustivel = SerializerMethodField()

    def get_nome_marca(self, obj):
        return obj.get_marca_display()

    def get_nome_cor(self, obj):
        return obj.get_cor_display()

    def get_nome_combustivel(self, obj):
        return obj.get_combustivel_display()

    class Meta:
        model = Veiculo
        fields = '__all__'
```

O padrão do professor usa `SerializerMethodField` para converter choices (números inteiros) em texto legível. Por exemplo, `marca = 7` vira `"nome_marca": "HONDA"`.

### `anuncio/serializers.py` (referência)

```python
from rest_framework.serializers import ModelSerializer
from .models import Anuncio

class SerializadorAnuncio(ModelSerializer):
    class Meta:
        model = Anuncio
        fields = '__all__'
```

## O que fazer

### 1. Criar o Serializer da Entidade Principal

Arquivo: `python/sistema/ENTIDADE_PRINCIPAL/serializers.py`

**Caso simples (sem choices):**
```python
from rest_framework.serializers import ModelSerializer
from .models import EntidadePrincipal

class SerializadorEntidadePrincipal(ModelSerializer):
    class Meta:
        model = EntidadePrincipal
        fields = '__all__'
```

**Caso com choices (igual ao professor):**
```python
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import EntidadePrincipal

class SerializadorEntidadePrincipal(ModelSerializer):
    nome_campo_choice = SerializerMethodField()

    def get_nome_campo_choice(self, obj):
        return obj.get_campo_choice_display()

    class Meta:
        model = EntidadePrincipal
        fields = '__all__'
```

### 2. Criar o Serializer da Entidade Secundária

Arquivo: `python/sistema/ENTIDADE_SECUNDARIA/serializers.py`

```python
from rest_framework.serializers import ModelSerializer
from .models import EntidadeSecundaria

class SerializadorEntidadeSecundaria(ModelSerializer):
    class Meta:
        model = EntidadeSecundaria
        fields = '__all__'
```

### 3. Conectar o Serializer à View API (já feito na Etapa 04)

As views já foram criadas na Etapa 04. Apenas confirme que o import está correto em `views.py`:

```python
from .serializers import SerializadorEntidadePrincipal

class APIListarEntidadePrincipal(ListAPIView):
    queryset = EntidadePrincipal.objects.all()
    serializer_class = SerializadorEntidadePrincipal
    permission_classes = [AllowAny]
```

### 4. Verificar a resposta JSON

```bash
python manage.py runserver
```

Acesse no navegador (ou Postman/Insomnia):
- `http://127.0.0.1:8000/ENTIDADE_PRINCIPAL/api/`
- `http://127.0.0.1:8000/ENTIDADE_SECUNDARIA/api/`

Deve retornar um array JSON com os dados do banco.

Exemplo de resposta esperada:
```json
[
  {
    "id": 1,
    "campo1": "valor",
    "campo2": "valor",
    "nome_campo_choice": "LABEL DO CHOICE",
    "criado_em": "2025-06-16T14:00:00Z",
    "atualizado_em": "2025-06-16T14:00:00Z"
  }
]
```

## Endpoint de Autenticação (já existe)

O endpoint `POST /autenticacao-api/` já está implementado pelo professor em `sistema/views.py` usando `ObtainAuthToken`. **Não precisa recriar**.

```python
class LoginAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.pk,
            'nome': user.get_full_name(),
            'email': user.email,
            'token': token.key
        })
```

## O que NÃO fazer nesta etapa

- Não adicione autenticação nas rotas de API ainda (deixe `AllowAny` como o professor)
- Não mexa no mobile ainda

## Verificação Final da Etapa

Checklist:
- [ ] `GET /ENTIDADE_PRINCIPAL/api/` retorna JSON
- [ ] `GET /ENTIDADE_SECUNDARIA/api/` retorna JSON
- [ ] `POST /autenticacao-api/` retorna token (testado com um usuário existente)
- [ ] CRUD web ainda funcionando

## Próxima Etapa

[Etapa 07 — Refatorar o App Mobile](07-etapa-app-mobile.md)
