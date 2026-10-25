# Ypetec

Sistema para que startups registrem informações sobre o seu desenvolvimento e as utilizem para validar a fase em que se encontram — substituindo o armazenamento atual em pastas do Google Drive.

> **Status:** Etapa 1 (front-end) — Fase 2 concluída: ambiente configurado. Nenhuma regra de negócio implementada.

## Tecnologias

- Python 3.12
- Django 5.2 LTS (Django Templates + sistema de rotas)
- HTML5, CSS3 (variáveis CSS) e JavaScript moderno (módulos ES, sem build)
- python-dotenv (variáveis de ambiente)
- SQLite (padrão do Django, apenas para inicialização)

## Pré-requisitos

- Python 3.12 (o launcher `py` do Windows já resolve a versão)
- Git

## Instalação

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Gere uma `DJANGO_SECRET_KEY` e cole no `.env`:

```powershell
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

## Execução

```powershell
python manage.py migrate
python manage.py runserver
```

Acesse <http://127.0.0.1:8000/>.

Testes:

```powershell
python manage.py test
```

## Configurações por ambiente

| Módulo | Uso |
|---|---|
| `config.settings.dev` | Padrão do `manage.py` (desenvolvimento local) |
| `config.settings.prod` | Padrão do `wsgi.py`/`asgi.py`; exige `DJANGO_ALLOWED_HOSTS` e HTTPS |

## Estrutura de diretórios

```text
config/           Projeto Django (settings separados por ambiente, urls, wsgi/asgi)
apps/core/        Páginas gerais (home, erros, guia de estilos)
templates/        base.html, layouts/, components/, pages/
static/           css/, js/ (main.js + components/), images/
docs/             Documentação de arquitetura
```

## Páginas implementadas

| Rota | Nome | Situação |
|---|---|---|
| `/` | `core:home` | Placeholder de verificação do ambiente |

## Pendências para a etapa de back-end

A definir conforme o escopo das telas for aprovado.
