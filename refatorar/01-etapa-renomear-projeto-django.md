# Etapa 01 — Renomear o Projeto Django

## Objetivo

Trocar o nome do projeto de `sistema` para o nome do seu projeto, e ajustar as configurações iniciais.

## Status

- [ ] Concluído

## Pré-condições

- Leu `docs/00-contexto-do-projeto.md` e definiu o domínio do projeto
- Backend funcionando com `python manage.py runserver`

## O que fazer

### 1. Renomear o projeto Django (opcional, mas recomendado)

O projeto Django se chama `sistema`. Dependendo do tema escolhido, pode valer renomear.

> **ATENÇÃO**: Renomear o projeto Django é trabalhoso pois o nome aparece em muitos lugares. Avalie se é necessário ou se mantém `sistema` como nome interno.

Se quiser renomear, os arquivos afetados são:
- `python/sistema/sistema/settings.py` → referências a `sistema`
- `python/sistema/sistema/urls.py`
- `python/sistema/sistema/wsgi.py` → `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')`
- `python/sistema/sistema/asgi.py`
- `python/sistema/manage.py` → `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')`

### 2. Atualizar `settings.py`

Arquivo: `python/sistema/sistema/settings.py`

Mudanças obrigatórias:
```python
# Trocar pelo nome do banco de dados do seu projeto
DATABASES = {
    'default': {
        ...
        'NAME': 'nome_do_seu_banco',  # era 'sistema'
        ...
    }
}

# Manter pt-br
LANGUAGE_CODE = 'pt-br'
```

### 3. Criar novo banco de dados no PostgreSQL

```sql
-- No psql ou pgAdmin
CREATE DATABASE nome_do_seu_banco;
```

### 4. Atualizar o `.env`

Arquivo: `python/sistema/.env`

```env
DATABASE_PASSWORD=sua_senha_postgres
```

### 5. Verificar funcionamento

```bash
cd python/sistema
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse `http://127.0.0.1:8000` — deve aparecer a tela de login.

## O que NÃO fazer nesta etapa

- Não mexa nos models ainda
- Não crie os novos apps ainda
- Não altere os templates ainda

## Próxima Etapa

[Etapa 02 — Criar os novos Apps Django](02-etapa-criar-apps-django.md)
