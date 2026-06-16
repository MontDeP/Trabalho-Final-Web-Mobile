# docs/ — Plano de Refatoração do Projeto

Esta pasta contém o plano completo para transformar o projeto do professor em um projeto próprio para a disciplina de Desenvolvimento Web e Mobile.

## Como usar esta pasta

1. **Leia sempre** `00-contexto-do-projeto.md` no início de cada sessão
2. **Abra o arquivo da etapa** que está trabalhando antes de começar qualquer modificação
3. **Marque como concluído** `- [x]` o status de cada etapa quando terminar
4. **Não pule etapas** — cada uma depende da anterior

## Etapas

| Arquivo | O que faz |
|---------|-----------|
| [00 — Contexto do Projeto](00-contexto-do-projeto.md) | O que é o projeto, o que muda, regras para não alucinar |
| [01 — Renomear o Projeto Django](01-etapa-renomear-projeto-django.md) | Configurar nome, banco de dados, `.env` |
| [02 — Criar os Apps Django](02-etapa-criar-apps-django.md) | `startapp`, registrar em `settings.py`, criar `urls.py` e `serializers.py` vazios |
| [03 — Criar os Models](03-etapa-criar-models.md) | Definir campos, FK, choices, auditoria, `__str__`, migrações |
| [04 — Criar Views e Forms](04-etapa-criar-views-e-forms.md) | ModelForm, CBV (ListView/CreateView/UpdateView/DeleteView), URLs, `form_valid` |
| [05 — Criar os Templates HTML](05-etapa-criar-templates.md) | Herança de `base.html`, `listar/novo/editar/deletar.html`, CSS |
| [06 — Criar a API REST](06-etapa-api-rest.md) | ModelSerializer, SerializerMethodField para choices, ListAPIView |
| [07 — Refatorar o App Mobile](07-etapa-app-mobile.md) | Services HTTP, provideHttpClient, login real, tela de listagem |
| [08 — Limpeza Final](08-etapa-limpeza-final.md) | Remover apps do professor, checklist de entrega, troubleshooting |

## Progresso

- [x] Etapa 01 — Renomear projeto Django
- [x] Etapa 02 — Criar os apps Django
- [x] Etapa 03 — Criar os models
- [x] Etapa 04 — Criar views e forms
- [x] Etapa 05 — Criar os templates HTML
- [x] Etapa 06 — Criar a API REST
- [x] Etapa 07 — Refatorar o app mobile
- [x] Etapa 08 — Limpeza final

## Contexto Rápido (para início de sessão)

**Stack:** Django 5.2 + PostgreSQL + DRF + Angular 19 + Ionic 8

**O que o professor fez:** Sistema de anúncios de veículos com:
- App `veiculo` — CRUD de carros com foto, marca, cor, combustível
- App `anuncio` — anúncio vinculado a um veículo e a um usuário
- Interface web via Django Templates
- API REST com Token Authentication para o mobile
- App mobile com tela de login (sem integração HTTP implementada)

**O que você vai fazer:** Mesmo sistema, mesmo padrão, mas com o seu domínio de negócio.

**Domínio escolhido:** _(preencher aqui após decisão)_

## Arquivos Críticos para Não Perder

| Arquivo | Por que é crítico |
|---------|-------------------|
| `python/sistema/sistema/settings.py` | Configuração central — apps instalados, banco, CORS |
| `python/sistema/sistema/urls.py` | Roteamento raiz — registra os apps |
| `python/sistema/sistema/views.py` | Login web e LoginAPI — não recriar, já funciona |
| `python/sistema/templates/base.html` | Base de todos os templates — menu e layout |
| `sistema-mobile/src/main.ts` | Ponto de entrada do Angular — adicionar `provideHttpClient()` aqui |
| `sistema-mobile/src/app/app.routes.ts` | Rotas do mobile — adicionar novas páginas aqui |
