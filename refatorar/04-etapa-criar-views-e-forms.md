# Etapa 04 — Criar os Forms e Views (CRUD Web)

## Objetivo

Criar os Forms (ModelForm) e as Class-Based Views para o CRUD completo das duas entidades, seguindo exatamente o padrão do professor.

## Status

- [ ] Concluído

## Referência: O que o professor fez

### `veiculo/forms.py` (referência)

```python
from django.forms import ModelForm
from .models import Veiculo

class VeiculoForm(ModelForm):
    class Meta:
        model = Veiculo
        fields = ['marca', 'modelo', 'ano', 'cor', 'combustivel', 'foto']
```

### `veiculo/views.py` — estrutura geral (referência)

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

class ListarVeiculos(LoginRequiredMixin, ListView):
    model = Veiculo
    template_name = 'veiculo/listar.html'
    context_object_name = 'veiculo'

class CadastrarVeiculos(LoginRequiredMixin, CreateView):
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'veiculo/novo.html'
    success_url = reverse_lazy('listar_veiculos')

class EditarVeiculos(LoginRequiredMixin, UpdateView):
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'veiculo/editar.html'
    success_url = reverse_lazy('listar_veiculos')

class DeletarVeiculos(LoginRequiredMixin, DeleteView):
    model = Veiculo
    template_name = 'veiculo/deletar.html'
    success_url = reverse_lazy('listar_veiculos')

class APIListarVeiculos(ListAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = SerializadorVeiculo
    permission_classes = [AllowAny]
```

### `anuncio/views.py` — diferença para o CreateView (referência)

No `CreateView` do anúncio, o professor sobrescreve `form_valid` para associar o usuário logado automaticamente:

```python
class CadastrarAnuncios(LoginRequiredMixin, CreateView):
    model = Anuncio
    form_class = AnuncioForm
    template_name = 'anuncio/novo.html'
    success_url = reverse_lazy('listar_anuncios')

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # <-- associa o usuário
        return super().form_valid(form)
```

## O que fazer

### 1. Criar o Form da Entidade Principal

Arquivo: `python/sistema/ENTIDADE_PRINCIPAL/forms.py`

```python
from django.forms import ModelForm
from .models import EntidadePrincipal

class EntidadePrincipalForm(ModelForm):
    class Meta:
        model = EntidadePrincipal
        fields = ['campo1', 'campo2', 'campo3']  # adaptar para seus campos
```

### 2. Criar o Form da Entidade Secundária

Arquivo: `python/sistema/ENTIDADE_SECUNDARIA/forms.py`

```python
from django.forms import ModelForm
from .models import EntidadeSecundaria

class EntidadeSecundariaForm(ModelForm):
    class Meta:
        model = EntidadeSecundaria
        fields = ['titulo', 'descricao', 'entidade_principal', 'preco']  # adaptar
        # NÃO incluir 'usuario' aqui — é associado automaticamente na view
```

### 3. Criar as Views da Entidade Principal

Arquivo: `python/sistema/ENTIDADE_PRINCIPAL/views.py`

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import EntidadePrincipal
from .forms import EntidadePrincipalForm
from .serializers import SerializadorEntidadePrincipal

class ListarEntidadePrincipal(LoginRequiredMixin, ListView):
    model = EntidadePrincipal
    template_name = 'ENTIDADE_PRINCIPAL/listar.html'
    context_object_name = 'itens'  # nome no template

class CadastrarEntidadePrincipal(LoginRequiredMixin, CreateView):
    model = EntidadePrincipal
    form_class = EntidadePrincipalForm
    template_name = 'ENTIDADE_PRINCIPAL/novo.html'
    success_url = reverse_lazy('listar_ENTIDADE_PRINCIPAL')

class EditarEntidadePrincipal(LoginRequiredMixin, UpdateView):
    model = EntidadePrincipal
    form_class = EntidadePrincipalForm
    template_name = 'ENTIDADE_PRINCIPAL/editar.html'
    success_url = reverse_lazy('listar_ENTIDADE_PRINCIPAL')

class DeletarEntidadePrincipal(LoginRequiredMixin, DeleteView):
    model = EntidadePrincipal
    template_name = 'ENTIDADE_PRINCIPAL/deletar.html'
    success_url = reverse_lazy('listar_ENTIDADE_PRINCIPAL')

class APIListarEntidadePrincipal(ListAPIView):
    queryset = EntidadePrincipal.objects.all()
    serializer_class = SerializadorEntidadePrincipal
    permission_classes = [AllowAny]
```

### 4. Criar as Views da Entidade Secundária

Arquivo: `python/sistema/ENTIDADE_SECUNDARIA/views.py`

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import EntidadeSecundaria
from .forms import EntidadeSecundariaForm
from .serializers import SerializadorEntidadeSecundaria

class ListarEntidadeSecundaria(LoginRequiredMixin, ListView):
    model = EntidadeSecundaria
    template_name = 'ENTIDADE_SECUNDARIA/listar.html'
    context_object_name = 'itens'

class CadastrarEntidadeSecundaria(LoginRequiredMixin, CreateView):
    model = EntidadeSecundaria
    form_class = EntidadeSecundariaForm
    template_name = 'ENTIDADE_SECUNDARIA/novo.html'
    success_url = reverse_lazy('listar_ENTIDADE_SECUNDARIA')

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # OBRIGATÓRIO
        return super().form_valid(form)

class EditarEntidadeSecundaria(LoginRequiredMixin, UpdateView):
    model = EntidadeSecundaria
    form_class = EntidadeSecundariaForm
    template_name = 'ENTIDADE_SECUNDARIA/editar.html'
    success_url = reverse_lazy('listar_ENTIDADE_SECUNDARIA')

class DeletarEntidadeSecundaria(LoginRequiredMixin, DeleteView):
    model = EntidadeSecundaria
    template_name = 'ENTIDADE_SECUNDARIA/deletar.html'
    success_url = reverse_lazy('listar_ENTIDADE_SECUNDARIA')

class APIListarEntidadeSecundaria(ListAPIView):
    queryset = EntidadeSecundaria.objects.all()
    serializer_class = SerializadorEntidadeSecundaria
    permission_classes = [AllowAny]
```

### 5. Criar as URLs de cada app

Arquivo: `python/sistema/ENTIDADE_PRINCIPAL/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.APIListarEntidadePrincipal.as_view(), name='api_ENTIDADE_PRINCIPAL'),
    path('', views.ListarEntidadePrincipal.as_view(), name='listar_ENTIDADE_PRINCIPAL'),
    path('novo/', views.CadastrarEntidadePrincipal.as_view(), name='novo_ENTIDADE_PRINCIPAL'),
    path('<int:pk>/', views.EditarEntidadePrincipal.as_view(), name='editar_ENTIDADE_PRINCIPAL'),
    path('deletar/<int:pk>/', views.DeletarEntidadePrincipal.as_view(), name='deletar_ENTIDADE_PRINCIPAL'),
]
```

Arquivo: `python/sistema/ENTIDADE_SECUNDARIA/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.APIListarEntidadeSecundaria.as_view(), name='api_ENTIDADE_SECUNDARIA'),
    path('', views.ListarEntidadeSecundaria.as_view(), name='listar_ENTIDADE_SECUNDARIA'),
    path('novo/', views.CadastrarEntidadeSecundaria.as_view(), name='novo_ENTIDADE_SECUNDARIA'),
    path('editar/<int:pk>/', views.EditarEntidadeSecundaria.as_view(), name='editar_ENTIDADE_SECUNDARIA'),
    path('deletar/<int:pk>/', views.DeletarEntidadeSecundaria.as_view(), name='deletar_ENTIDADE_SECUNDARIA'),
]
```

### 6. Registrar as URLs no `urls.py` raiz

Arquivo: `python/sistema/sistema/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('autenticacao-api/', views.LoginAPI.as_view(), name='autenticacao_api'),
    # seus novos apps (substituir os do professor)
    path('ENTIDADE_PRINCIPAL/', include('ENTIDADE_PRINCIPAL.urls')),
    path('ENTIDADE_SECUNDARIA/', include('ENTIDADE_SECUNDARIA.urls')),
]
```

## Verificação

```bash
python manage.py check
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/ENTIDADE_PRINCIPAL/` — deve redirecionar para login (LoginRequiredMixin funcionando).

## O que NÃO fazer nesta etapa

- Não crie os templates ainda (próxima etapa)
- Não mexa no app mobile ainda
- Os serializers serão criados na etapa de API REST

## Próxima Etapa

[Etapa 05 — Criar os Templates HTML](05-etapa-criar-templates.md)
