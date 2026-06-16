# Guia de Recriação do Repositório `web_mobile`

Este guia descreve como recriar o repositório do zero em um repositório vazio, mantendo a mesma estrutura, configurações e funcionalidades.

---

## Visão Geral do Projeto

O repositório contém três partes independentes:

| Pasta | Descrição | Tecnologias |
|---|---|---|
| `html-css-js/` | Exemplos de aulas de HTML/CSS/Bootstrap | HTML, CSS, Bootstrap 5, jQuery, JS |
| `python/` | Backend (API + Interface Web) | Django 5.2, DRF, PostgreSQL |
| `sistema-mobile/` | Frontend Mobile | Angular 19, Ionic 8, Capacitor 7 |

---

## Pré-requisitos

Instale as ferramentas antes de começar:

- **Git** — https://git-scm.com/
- **Python 3.11+** — https://www.python.org/
- **Node.js 18+** — https://nodejs.org/
- **PostgreSQL 14+** — https://www.postgresql.org/
- **Ionic CLI** — `npm install -g @ionic/cli`
- **Angular CLI** — `npm install -g @angular/cli`

---

## Passo 1 — Inicializar o Repositório

```bash
# Criar e entrar na pasta do novo repositório
mkdir web_mobile
cd web_mobile

# Inicializar o git
git init

# (Opcional) Conectar ao repositório remoto
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
```

---

## Passo 2 — Criar o `.gitignore` na Raiz

Crie o arquivo `.gitignore` na raiz do repositório com o seguinte conteúdo:

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so
# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
# PyInstaller
*.manifest
*.spec
# Installer logs
pip-log.txt
pip-delete-this-directory.txt
# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/
# Translations
*.mo
*.pot
# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
# Flask stuff:
instance/
.webassets-cache
# Scrapy stuff:
.scrapy
# Sphinx documentation
docs/_build/
# PyBuilder
.pybuilder/
target/
# Jupyter Notebook
.ipynb_checkpoints
# IPython
profile_default/
ipython_config.py
.pdm.toml
.pdm-python
.pdm-build/
__pypackages__/
celerybeat-schedule
celerybeat.pid
*.sage.py
# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
virtual/
/python/virtual/
# Spyder project settings
.spyderproject
.spyproject
# Rope project settings
.ropeproject
# mkdocs documentation
/site
# mypy
.mypy_cache/
.dmypy.json
dmypy.json
# Pyre type checker
.pyre/
# pytype static type analyzer
.pytype/
# Cython debug symbols
cython_debug/
# Ruff stuff:
.ruff_cache/
.pypirc
.vscode/
*.jpg
*.png
*.jpeg
*.webp
# compiled output
/dist
/tmp
/out-tsc
# dependencies
/node_modules
# IDEs and editors
/.idea
.project
.classpath
.c9/
*.launch
.settings/
*.sublime-workspace
# IDE - VSCode
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
# misc
/.sass-cache
/connect.lock
/coverage
/libpeerconnection.log
npm-debug.log
testem.log
/typings
# e2e
/e2e/*.js
/e2e/*.map
# System Files
.DS_Store
Thumbs.db
*~
*.sw[mnpcod]
.tmp
*.tmp
*.tmp.*
UserInterfaceState.xcuserstate
$RECYCLE.BIN/
log.txt
/.sourcemaps
/.versions
# Ionic
/.ionic
/www
/platforms
/plugins
# Compiled output
/bazel-out
# Node
yarn-error.log
.idea/
*.sublime-project
# Visual Studio Code
.history/*
# Miscellaneous
/.angular
/.angular/cache
.sass-cache/
/.nx
/.nx/cache
```

---

## Passo 3 — Criar a Pasta `html-css-js/`

### Estrutura esperada

```
html-css-js/
├── aula-1.html
├── aula-2.html
├── css/
│   ├── styles.css
│   └── [arquivos Bootstrap 5]
├── js/
│   ├── funcoes.js
│   ├── jquery.js
│   └── [arquivos Bootstrap 5 JS]
└── imgs/
    └── brasao_uft.png
```

### Bootstrap 5

Baixe o Bootstrap 5 em https://getbootstrap.com/docs/5.0/getting-started/download/ e extraia os arquivos `css/` e `js/` para as respectivas pastas.

Os arquivos necessários em `css/`:
- `bootstrap.css`, `bootstrap.min.css`, `bootstrap.css.map`, `bootstrap.min.css.map`
- `bootstrap.rtl.css`, `bootstrap.rtl.min.css`
- `bootstrap-grid.css`, `bootstrap-grid.min.css`
- `bootstrap-reboot.css`, `bootstrap-reboot.min.css`
- `bootstrap-utilities.css`, `bootstrap-utilities.min.css`
- `styles.css` (arquivo customizado — criar vazio ou copiar estilos das aulas)

Os arquivos necessários em `js/`:
- `bootstrap.js`, `bootstrap.min.js`, `bootstrap.js.map`
- `bootstrap.bundle.js`, `bootstrap.bundle.min.js`
- `bootstrap.esm.js`, `bootstrap.esm.min.js`
- `jquery.js` (baixar em https://jquery.com/download/)
- `funcoes.js` (arquivo customizado das aulas)

---

## Passo 4 — Criar o Backend Django (`python/`)

### 4.1 — Criar o ambiente virtual

```bash
cd python
python -m venv virtual
```

### 4.2 — Ativar o ambiente e instalar dependências

**Windows (PowerShell):**
```powershell
.\virtual\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.\virtual\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source virtual/bin/activate
```

Instalar os pacotes:
```bash
pip install django==5.2
pip install djangorestframework
pip install django-cors-headers
pip install python-dotenv
pip install psycopg2-binary
```

### 4.3 — Criar o projeto Django

```bash
cd python
django-admin startproject sistema
cd sistema
```

### 4.4 — Criar os apps

```bash
python manage.py startapp veiculo
python manage.py startapp anuncio
```

### 4.5 — Configurar `settings.py`

Edite `python/sistema/sistema/settings.py` com as seguintes configurações principais:

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-TROQUE-ESTA-CHAVE-EM-PRODUCAO'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Libs
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    # Apps
    'veiculo',
    'anuncio',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sistema.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sistema.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sistema',
        'USER': 'postgres',
        'PASSWORD': 'SUA_SENHA_AQUI',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'sistema/static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

LOGIN_URL = '/autenticacao/'
LOGIN_REDIRECT_URL = '/veiculo/listar/'
LOGOUT_REDIRECT_URL = '/autenticacao/'
```

### 4.6 — Configurar `urls.py` principal

Arquivo `python/sistema/sistema/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autenticacao/', views.autenticacao, name='autenticacao'),
    path('sair/', views.sair, name='sair'),
    path('veiculo/', include('veiculo.urls')),
    path('anuncio/', include('anuncio.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 4.7 — Views de autenticação (`sistema/views.py`)

Arquivo `python/sistema/sistema/views.py`:

```python
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def autenticacao(request):
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('senha')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('listar_veiculo')
        else:
            return render(request, 'autenticacao.html', {'erro': 'Usuário ou senha inválidos'})
    return render(request, 'autenticacao.html')

def sair(request):
    logout(request)
    return redirect('autenticacao')
```

### 4.8 — App `veiculo`

**`veiculo/models.py`:**
```python
from django.db import models
from .consts import MARCAS, CORES, COMBUSTIVEIS

class Veiculo(models.Model):
    marca = models.CharField(max_length=50, choices=MARCAS)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    cor = models.CharField(max_length=30, choices=CORES)
    combustivel = models.CharField(max_length=20, choices=COMBUSTIVEIS)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quilometragem = models.IntegerField()
    foto = models.ImageField(upload_to='veiculo/fotos/', null=True, blank=True)

    def __str__(self):
        return f'{self.marca} {self.modelo} ({self.ano})'
```

**`veiculo/consts.py`:**
```python
MARCAS = [
    ('chevrolet', 'Chevrolet'),
    ('ford', 'Ford'),
    ('volkswagen', 'Volkswagen'),
    ('fiat', 'Fiat'),
    ('honda', 'Honda'),
    ('toyota', 'Toyota'),
    ('hyundai', 'Hyundai'),
    ('nissan', 'Nissan'),
    ('renault', 'Renault'),
    ('jeep', 'Jeep'),
]

CORES = [
    ('branco', 'Branco'),
    ('preto', 'Preto'),
    ('prata', 'Prata'),
    ('cinza', 'Cinza'),
    ('vermelho', 'Vermelho'),
    ('azul', 'Azul'),
]

COMBUSTIVEIS = [
    ('gasolina', 'Gasolina'),
    ('etanol', 'Etanol'),
    ('flex', 'Flex'),
    ('diesel', 'Diesel'),
    ('eletrico', 'Elétrico'),
    ('hibrido', 'Híbrido'),
]
```

**`veiculo/forms.py`:**
```python
from django import forms
from .models import Veiculo

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'
```

**`veiculo/serializers.py`:**
```python
from rest_framework import serializers
from .models import Veiculo

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = '__all__'
```

**`veiculo/urls.py`:**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('listar/', views.listar, name='listar_veiculo'),
    path('novo/', views.novo, name='novo_veiculo'),
    path('editar/<int:id>/', views.editar, name='editar_veiculo'),
    path('deletar/<int:id>/', views.deletar, name='deletar_veiculo'),
    path('api/', views.VeiculoAPIView.as_view(), name='api_veiculo'),
    path('api/<int:pk>/', views.VeiculoDetailAPIView.as_view(), name='api_veiculo_detail'),
]
```

**`veiculo/admin.py`:**
```python
from django.contrib import admin
from .models import Veiculo

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'ano', 'cor', 'preco')
    list_filter = ('marca', 'cor', 'combustivel')
    search_fields = ('modelo', 'marca')
```

### 4.9 — App `anuncio`

**`anuncio/models.py`:**
```python
from django.db import models
from veiculo.models import Veiculo

class Anuncio(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    descricao = models.TextField()
    data_publicacao = models.DateField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'Anúncio - {self.veiculo}'
```

**`anuncio/forms.py`:**
```python
from django import forms
from .models import Anuncio

class AnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = '__all__'
```

**`anuncio/serializers.py`:**
```python
from rest_framework import serializers
from .models import Anuncio

class AnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anuncio
        fields = '__all__'
```

**`anuncio/urls.py`:**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('listar/', views.listar, name='listar_anuncio'),
    path('novo/', views.novo, name='novo_anuncio'),
    path('editar/<int:id>/', views.editar, name='editar_anuncio'),
    path('deletar/<int:id>/', views.deletar, name='deletar_anuncio'),
    path('api/', views.AnuncioAPIView.as_view(), name='api_anuncio'),
    path('api/<int:pk>/', views.AnuncioDetailAPIView.as_view(), name='api_anuncio_detail'),
]
```

### 4.10 — Banco de dados (PostgreSQL)

```sql
-- Executar no psql como superusuário
CREATE DATABASE sistema;
CREATE USER postgres WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE sistema TO postgres;
```

### 4.11 — Executar migrations e criar superusuário

```bash
cd python/sistema
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4.12 — Iniciar o servidor Django

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/autenticacao/

---

## Passo 5 — Criar o Frontend Mobile Ionic (`sistema-mobile/`)

### 5.1 — Criar o projeto Ionic

```bash
ionic start sistema-mobile blank --type=angular --standalone
cd sistema-mobile
```

> Selecione **Angular standalone** quando perguntado.

### 5.2 — Instalar dependências adicionais

```bash
npm install @ionic/storage-angular
npm install @capacitor/app @capacitor/haptics @capacitor/keyboard @capacitor/status-bar
```

### 5.3 — Estrutura do projeto mobile

```
sistema-mobile/
├── src/
│   ├── app/
│   │   ├── app.component.ts        (componente raiz standalone)
│   │   ├── app.component.html
│   │   ├── app.component.scss
│   │   ├── app.routes.ts           (rotas da aplicação)
│   │   └── home/
│   │       ├── home.page.ts        (página de login)
│   │       ├── home.page.html
│   │       └── home.page.scss
│   ├── assets/
│   ├── environments/
│   │   ├── environment.ts          (config de desenvolvimento)
│   │   └── environment.prod.ts     (config de produção)
│   └── theme/
│       └── variables.scss
```

### 5.4 — Configurar `environment.ts`

Arquivo `src/environments/environment.ts`:
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://127.0.0.1:8000'
};
```

Arquivo `src/environments/environment.prod.ts`:
```typescript
export const environment = {
  production: true,
  apiUrl: 'http://SEU_SERVIDOR_PRODUCAO'
};
```

### 5.5 — Configurar `app.routes.ts`

```typescript
import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then(m => m.HomePage),
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
];
```

### 5.6 — Configurar `capacitor.config.ts`

```typescript
import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'io.ionic.starter',
  appName: 'sistema-mobile',
  webDir: 'www',
  plugins: {
    SplashScreen: {
      launchShowDuration: 0,
    },
  },
};

export default config;
```

### 5.7 — Iniciar o app mobile

```bash
cd sistema-mobile
npm install
ionic serve
```

Acesse: http://localhost:8100

---

## Passo 6 — Estrutura Final de Pastas

Após todos os passos, a estrutura deve ser:

```
web_mobile/
├── .gitignore
├── docs/
│   └── guia-recriacao-repositorio.md
├── html-css-js/
│   ├── aula-1.html
│   ├── aula-2.html
│   ├── css/
│   │   └── [arquivos Bootstrap + styles.css]
│   ├── js/
│   │   └── [arquivos Bootstrap + jquery.js + funcoes.js]
│   └── imgs/
│       └── brasao_uft.png
├── python/
│   ├── virtual/                    (ignorado pelo .gitignore)
│   └── sistema/
│       ├── manage.py
│       ├── sistema/
│       │   ├── __init__.py
│       │   ├── settings.py
│       │   ├── urls.py
│       │   ├── views.py
│       │   ├── wsgi.py
│       │   └── asgi.py
│       ├── veiculo/
│       │   ├── migrations/
│       │   ├── admin.py
│       │   ├── apps.py
│       │   ├── consts.py
│       │   ├── forms.py
│       │   ├── models.py
│       │   ├── serializers.py
│       │   ├── tests.py
│       │   ├── urls.py
│       │   └── views.py
│       ├── anuncio/
│       │   ├── migrations/
│       │   ├── admin.py
│       │   ├── apps.py
│       │   ├── forms.py
│       │   ├── models.py
│       │   ├── serializers.py
│       │   ├── tests.py
│       │   ├── urls.py
│       │   └── views.py
│       └── templates/
│           ├── base.html
│           ├── autenticacao.html
│           ├── veiculo/
│           │   ├── listar.html
│           │   ├── novo.html
│           │   ├── editar.html
│           │   └── deletar.html
│           └── anuncio/
│               ├── listar.html
│               ├── novo.html
│               ├── editar.html
│               └── deletar.html
└── sistema-mobile/
    ├── package.json
    ├── angular.json
    ├── ionic.config.json
    ├── capacitor.config.ts
    ├── tsconfig.json
    └── src/
        └── [conforme descrito no Passo 5]
```

---

## Versões Utilizadas

| Tecnologia | Versão |
|---|---|
| Python | 3.11+ |
| Django | 5.2 |
| djangorestframework | última estável |
| django-cors-headers | última estável |
| psycopg2-binary | última estável |
| PostgreSQL | 14+ |
| Node.js | 18+ |
| Angular | 19.0.0 |
| Ionic Framework | 8.0.0 |
| Capacitor | 7.2.0 |
| TypeScript | 5.6.3 |
| RxJS | 7.8.0 |
| Bootstrap | 5.x |
| jQuery | 3.x |

---

## Observações Importantes

- O arquivo `db.sqlite3` é ignorado pelo `.gitignore` — o banco de dados **não é versionado**
- A pasta `python/virtual/` (ambiente virtual) é ignorada — execute `pip install` sempre após clonar
- A pasta `node_modules/` é ignorada — execute `npm install` sempre após clonar
- Imagens (`.jpg`, `.png`, `.jpeg`, `.webp`) são ignoradas pelo `.gitignore`
- O arquivo `sistema-mobile/.gitignore` tem regras adicionais específicas para o projeto Angular/Ionic
