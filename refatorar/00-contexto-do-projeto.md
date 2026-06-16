# Contexto do Projeto — O que é e por que refatorar

## Situação Atual

Este repositório contém o **projeto do professor** da disciplina de Desenvolvimento Web e Mobile. O sistema implementa um marketplace de anúncios de veículos, construído aula a aula ao longo do semestre.

O professor criou este sistema para demonstrar as tecnologias:
- Django 5.2 com PostgreSQL
- Django REST Framework com Token Authentication
- Angular 19 + Ionic 8 (app mobile)

## Objetivo da Refatoração

O professor quer que o aluno **reimplemente o mesmo sistema — usando exatamente a mesma stack e metodologia ensinada — mas com um domínio de negócio próprio**.

Ou seja: trocar "veículos e anúncios" por outro tema, mantendo toda a arquitetura, padrões de código e fluxos iguais.

## O que NÃO muda

- Stack: Django + PostgreSQL + DRF + Ionic/Angular
- Padrões: MTV, CBV, ModelSerializer, Standalone Components
- Arquitetura: Backend API REST + Interface Web + App Mobile
- Fluxos: autenticação web por sessão, autenticação mobile por token
- Estrutura de templates: herança com base.html
- Admin customizado
- CORS configurado para o mobile consumir a API

## O que MUDA

- Nome do projeto
- Domínio de negócio (ex: livros, imóveis, jogos, produtos, etc.)
- Modelos (campos e relações do novo domínio)
- Templates (visual e nomenclatura)
- URLs e names das rotas
- Serializers (campos do novo domínio)
- Constantes e choices (se aplicável)
- Nome do app mobile e identidade visual

## Domínio Escolhido

**Catálogo de Jogos**

- App principal: `jogo` — campos: titulo, plataforma, genero, ano, desenvolvedor, foto
- App secundário: `avaliacao` — campos: titulo, descricao, jogo (FK), usuario (FK), nota

## Regras para Não Alucinar

Ao iniciar uma sessão de refatoração, leia SEMPRE este arquivo e o arquivo da etapa que vai trabalhar (`docs/etapa-XX-*.md`) ANTES de começar qualquer modificação. O plano em `docs/` é a fonte da verdade — não improvise, não adicione funcionalidades que não estão listadas.

---

## Links dos Arquivos Principais

| Arquivo | Caminho |
|---------|---------|
| Settings Django | `python/sistema/sistema/settings.py` |
| URLs raiz | `python/sistema/sistema/urls.py` |
| Views de auth | `python/sistema/sistema/views.py` |
| Model Veiculo | `python/sistema/veiculo/models.py` |
| Model Anuncio | `python/sistema/anuncio/models.py` |
| Serializer Veiculo | `python/sistema/veiculo/serializers.py` |
| Serializer Anuncio | `python/sistema/anuncio/serializers.py` |
| Template base | `python/sistema/templates/base.html` |
| App mobile raiz | `sistema-mobile/src/app/` |
| Rotas mobile | `sistema-mobile/src/app/app.routes.ts` |
| Home page mobile | `sistema-mobile/src/app/home/home.page.ts` |
