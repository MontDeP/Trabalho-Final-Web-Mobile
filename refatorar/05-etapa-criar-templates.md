# Etapa 05 — Criar os Templates HTML

## Objetivo

Criar os templates HTML das novas entidades, usando herança de `base.html` exatamente como o professor ensinou.

## Status

- [ ] Concluído

## Como funciona a herança de templates no projeto

O professor criou um `base.html` com a estrutura geral (header, menu, footer). Todos os outros templates herdam dele usando `{% extends 'base.html' %}` e sobrescrevem o bloco `{% block conteudo %}`.

Estrutura de templates atual:
```
templates/
├── base.html               ← template base (NÃO apagar ou modificar antes de entender)
├── autenticacao.html       ← tela de login (não mexer)
├── veiculo/
│   ├── listar.html
│   ├── novo.html
│   ├── editar.html
│   └── deletar.html
└── anuncio/
    ├── listar.html
    ├── novo.html
    ├── editar.html
    └── deletar.html
```

## O que fazer

### 1. Criar as pastas de templates dos seus apps

```
templates/
└── ENTIDADE_PRINCIPAL/
    ├── listar.html
    ├── novo.html
    ├── editar.html
    └── deletar.html
└── ENTIDADE_SECUNDARIA/
    ├── listar.html
    ├── novo.html
    ├── editar.html
    └── deletar.html
```

### 2. Template `listar.html` da Entidade Principal

Arquivo: `python/sistema/templates/ENTIDADE_PRINCIPAL/listar.html`

Baseie-se em `templates/veiculo/listar.html`. O padrão é:

```html
{% extends 'base.html' %}
{% load static %}

{% block conteudo %}
<div class="container">
    <div class="header-lista">
        <h2>Lista de [Nome da Entidade]</h2>
        <a href="{% url 'novo_ENTIDADE_PRINCIPAL' %}" class="btn-novo">Novo</a>
    </div>

    <div class="grid-cards">
        {% for item in itens %}
        <div class="card">
            <!-- Se tiver foto: -->
            {% if item.foto %}
            <img src="{% url 'foto_ENTIDADE_PRINCIPAL' item.foto.name %}" alt="{{ item }}">
            {% endif %}

            <div class="card-info">
                <h3>{{ item }}</h3>
                <!-- campos do seu domínio -->
                <p>{{ item.campo1 }}</p>
                <p>{{ item.campo2 }}</p>
            </div>

            <div class="card-acoes">
                <a href="{% url 'editar_ENTIDADE_PRINCIPAL' item.pk %}">Editar</a>
                <a href="{% url 'deletar_ENTIDADE_PRINCIPAL' item.pk %}">Excluir</a>
            </div>
        </div>
        {% empty %}
        <p>Nenhum item cadastrado.</p>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

### 3. Template `novo.html`

Arquivo: `python/sistema/templates/ENTIDADE_PRINCIPAL/novo.html`

```html
{% extends 'base.html' %}
{% load static %}

{% block conteudo %}
<div class="container form-container">
    <h2>Novo [Nome da Entidade]</h2>

    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Salvar</button>
        <a href="{% url 'listar_ENTIDADE_PRINCIPAL' %}">Cancelar</a>
    </form>
</div>
{% endblock %}
```

> **IMPORTANTE**: `enctype="multipart/form-data"` é obrigatório SOMENTE se o form tiver upload de arquivo (ImageField, FileField). Se não tiver, pode omitir.

### 4. Template `editar.html`

Arquivo: `python/sistema/templates/ENTIDADE_PRINCIPAL/editar.html`

Idêntico ao `novo.html`, mas com título diferente:

```html
{% extends 'base.html' %}
{% load static %}

{% block conteudo %}
<div class="container form-container">
    <h2>Editar [Nome da Entidade]</h2>

    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Salvar</button>
        <a href="{% url 'listar_ENTIDADE_PRINCIPAL' %}">Cancelar</a>
    </form>
</div>
{% endblock %}
```

### 5. Template `deletar.html`

Arquivo: `python/sistema/templates/ENTIDADE_PRINCIPAL/deletar.html`

```html
{% extends 'base.html' %}

{% block conteudo %}
<div class="container">
    <h2>Confirmar Exclusão</h2>
    <p>Tem certeza que deseja excluir <strong>{{ object }}</strong>?</p>

    <form method="post">
        {% csrf_token %}
        <button type="submit">Confirmar Exclusão</button>
        <a href="{% url 'listar_ENTIDADE_PRINCIPAL' %}">Cancelar</a>
    </form>
</div>
{% endblock %}
```

### 6. Criar os mesmos 4 templates para a Entidade Secundária

Repita os passos 2–5 para `ENTIDADE_SECUNDARIA`, adaptando os campos para exibir dados do seu domínio.

No template `listar.html` da entidade secundária, exiba os dados da entidade principal associada:
```html
<p>{{ item.entidade_principal }}</p>
<p>Autor: {{ item.usuario.username }}</p>
```

### 7. Atualizar o `base.html` com novos links de menu

Arquivo: `python/sistema/templates/base.html`

Adicione os links de menu para as novas entidades (e remova ou comente os do professor):

```html
<nav>
    <a href="{% url 'listar_ENTIDADE_PRINCIPAL' %}">ENTIDADE PRINCIPAL</a>
    <a href="{% url 'listar_ENTIDADE_SECUNDARIA' %}">ENTIDADE SECUNDÁRIA</a>
    <a href="{% url 'logout' %}">Sair</a>
</nav>
```

## Verificação

```bash
python manage.py runserver
```

Faça o ciclo completo:
1. Login em `http://127.0.0.1:8000`
2. Acesse a listagem da entidade principal
3. Crie um novo item
4. Edite o item criado
5. Exclua o item

## CSS

Crie os arquivos CSS em `python/sistema/sistema/static/css/` seguindo o mesmo padrão do professor:
- `listar.css` — estilo dos cards da listagem
- `novo.css` — estilo dos formulários de criação
- `editar.css` — estilo dos formulários de edição
- `deletar.css` — estilo da confirmação de exclusão

Carregue os CSS nos templates com:
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/listar.css' %}">
```

## O que NÃO fazer nesta etapa

- Não mexa nos serializers ainda
- Não mexa no app mobile ainda

## Próxima Etapa

[Etapa 06 — Criar a API REST com DRF](06-etapa-api-rest.md)
