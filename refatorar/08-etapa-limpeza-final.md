# Etapa 08 — Limpeza Final e Revisão

## Objetivo

Remover os apps do professor, fazer a limpeza do código, verificar o sistema completo e preparar para entrega.

## Status

- [ ] Concluído

## Pré-condições

Antes de iniciar esta etapa, confirme que:
- [ ] CRUD web da Entidade Principal funciona completamente
- [ ] CRUD web da Entidade Secundária funciona completamente
- [ ] `GET /ENTIDADE_PRINCIPAL/api/` retorna JSON correto
- [ ] `GET /ENTIDADE_SECUNDARIA/api/` retorna JSON correto
- [ ] Login mobile conecta ao backend e navega para a lista
- [ ] Lista mobile exibe dados reais do banco

## O que fazer

### 1. Remover os apps do professor de `settings.py`

Arquivo: `python/sistema/sistema/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # REMOVER estas linhas:
    # 'veiculo.apps.VeiculoConfig',
    # 'anuncio.apps.AnuncioConfig',
    # MANTER seus apps:
    'ENTIDADE_PRINCIPAL.apps.EntidadePrincipalConfig',
    'ENTIDADE_SECUNDARIA.apps.EntidadeSecundariaConfig',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken'
]
```

### 2. Remover as URLs dos apps do professor

Arquivo: `python/sistema/sistema/urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('autenticacao-api/', views.LoginAPI.as_view(), name='autenticacao_api'),
    # REMOVER:
    # path('veiculo/', include('veiculo.urls')),
    # path('anuncio/', include('anuncio.urls')),
    # MANTER:
    path('ENTIDADE_PRINCIPAL/', include('ENTIDADE_PRINCIPAL.urls')),
    path('ENTIDADE_SECUNDARIA/', include('ENTIDADE_SECUNDARIA.urls')),
]
```

### 3. Verificar se pode apagar as pastas dos apps do professor

> **ATENÇÃO**: Só apague as pastas `veiculo/` e `anuncio/` se tiver certeza que:
> - Nenhuma migração sua referencia modelos deles
> - Nenhum template seu usa `{% url 'listar_veiculos' %}` ou similares
> - O banco de dados não tem dados relevantes nessas tabelas

Para verificar dependências:
```bash
# Procurar referências aos apps do professor nos seus arquivos
grep -r "veiculo" python/sistema/ENTIDADE_PRINCIPAL/
grep -r "anuncio" python/sistema/ENTIDADE_SECUNDARIA/
grep -r "veiculo" python/sistema/templates/ENTIDADE_PRINCIPAL/
```

Se não houver referências, pode apagar com segurança.

### 4. Atualizar `LOGIN_URL` em `settings.py`

Verifique se o redirecionamento após login aponta para a sua entidade:

Arquivo: `python/sistema/sistema/views.py`

```python
class Login(View):
    def post(self, request):
        # ...
        if usuario:
            login(request, usuario)
            return redirect('listar_ENTIDADE_PRINCIPAL')  # atualizar aqui
```

### 5. Verificar migrações órfãs

```bash
cd python/sistema
python manage.py showmigrations
```

Se aparecerem migrações de `veiculo` ou `anuncio` que não foram aplicadas ainda, aplique-as ou remova-as antes de apagar as pastas.

### 6. Verificar `base.html`

Arquivo: `python/sistema/templates/base.html`

- Confirme que os links do menu apontam para as suas rotas
- Remova referências a `veiculo` e `anuncio`
- Atualize o título e identidade visual para o seu projeto

### 7. Checar o `base.html` para o redirect inicial

Arquivo: `python/sistema/sistema/views.py`

```python
class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('listar_ENTIDADE_PRINCIPAL')  # adaptar
        return render(request, 'autenticacao.html')
```

### 8. Teste completo do sistema

Execute o ciclo completo uma vez para confirmar que tudo funciona:

**Backend Web:**
1. `python manage.py runserver`
2. Acesse `http://127.0.0.1:8000`
3. Faça login
4. Crie um item na Entidade Principal
5. Crie um item na Entidade Secundária vinculando o anterior
6. Edite ambos
7. Exclua um
8. Teste `GET /ENTIDADE_PRINCIPAL/api/` no navegador
9. Teste `GET /ENTIDADE_SECUNDARIA/api/` no navegador

**Backend API (Postman/Insomnia):**
1. `POST http://127.0.0.1:8000/autenticacao-api/` com `{ "username": "...", "password": "..." }`
2. Copie o token retornado
3. `GET http://127.0.0.1:8000/ENTIDADE_PRINCIPAL/api/` — deve retornar dados

**App Mobile:**
1. `ionic serve`
2. Abra `http://localhost:8100`
3. Login com usuário existente
4. Confirme que navega e exibe a lista

### 9. Revisar o README.md

Atualize o `README.md` na raiz do projeto com:
- Nome e descrição do seu projeto
- Seus modelos (campos e relações)
- Suas URLs/endpoints
- Como executar

---

## Checklist Final de Entrega

### Backend Django
- [ ] Apps do professor removidos de `settings.py`
- [ ] URLs do professor removidas de `urls.py`
- [ ] Dois apps criados com seus próprios modelos
- [ ] Migrações aplicadas e banco com dados de teste
- [ ] CRUD completo funcionando (listar, criar, editar, deletar)
- [ ] API REST retornando JSON correto para as duas entidades
- [ ] Autenticação via Token funcionando (`/autenticacao-api/`)
- [ ] Admin funcionando com as duas entidades registradas
- [ ] Templates com identidade visual do seu projeto

### Frontend Mobile
- [ ] Nome do app atualizado
- [ ] `environment.ts` configurado com URL correta
- [ ] Tela de login fazendo requisição HTTP real
- [ ] Token armazenado no `Ionic Storage`
- [ ] Tela de listagem consumindo a API com token
- [ ] Navegação funcional (login → lista)

### Código
- [ ] Sem referências a `veiculo` ou `anuncio` nos seus arquivos
- [ ] Sem `console.log` de debug esquecidos
- [ ] README atualizado

---

## Problemas Conhecidos que Podem Surgir

### CORS erro no mobile
Se o mobile não consegue conectar ao backend:
1. Confirme que `corsheaders` está em `INSTALLED_APPS`
2. Confirme que `'corsheaders.middleware.CorsMiddleware'` está em `MIDDLEWARE`
3. Confirme que `CORS_ORIGIN_ALLOW_ALL = True` está em `settings.py`

### Token inválido / 401
1. Verifique se `rest_framework.authtoken` está em `INSTALLED_APPS`
2. Execute `python manage.py migrate` (cria a tabela de tokens)
3. Verifique o header: `Authorization: Token <token>` (com espaço, não dois pontos)

### ImageField não salva foto
1. Verifique se `Pillow` está instalado: `pip install Pillow`
2. Confirme `enctype="multipart/form-data"` no form HTML
3. Confirme o diretório de upload existe ou será criado pelo Django
