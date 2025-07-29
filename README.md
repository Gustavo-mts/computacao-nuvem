# Nome do Seu Projeto

## Descrição do Projeto
Sistema web desenvolvido em Python/FastAPI para gerenciar abrigos e pessoas em situação de vulnerabilidade social.

Funcionalidades
API RESTful: Construído com FastAPI para uma comunicação eficiente e estruturada.

Persistência de Dados: Utiliza PostgreSQL para armazenamento seguro e escalável de informações.

## Pré-requisitos
Antes de iniciar o projeto, certifique-se de ter as seguintes ferramentas instaladas em sua máquina:

- **Docker**: [Instalação do Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: Geralmente vem junto com a instalação do Docker Desktop. Caso contrário, siga as [instruções de instalação do Docker Compose](https://docs.docker.com/compose/install/).

## Primeiros Passos
Siga estas instruções para configurar e executar o projeto em sua máquina local.

### 1. Clonar o Repositório
Primeiro, clone este repositório para o seu ambiente local:

```bash
git clone https://github.com/Gustavo-mts/computacao-nuvem.git
cd https://github.com/Gustavo-mts/computacao-nuvem
```

## 2. Configuração das Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para a configuração do banco de dados e outros parâmetros. As variáveis estão definidas no `compose.yaml` e no `Dockerfile`.

**ATENÇÃO**: No seu `compose.yaml` e `Dockerfile`, a senha do banco de dados está definida como `sua_senha_aqui`. Para fins de segurança e para que o banco de dados funcione corretamente, você **DEVE** substituir `sua_senha_aqui` por uma senha forte e real em ambos os arquivos.

### `compose.yaml` (parte do serviço db e app):

```yaml
services:
  app:
    # ...
    environment:
      DATABASE_URL: postgresql://homeless_user:SUA_SENHA_FORTE_AQUI@db:5432/homeless_db
      DB_PASSWORD: SUA_SENHA_FORTE_AQUI # Certifique-se que esta senha é a mesma da DATABASE_URL

  db:
    # ...
    environment:
      POSTGRES_PASSWORD: SUA_SENHA_FORTE_AQUI # ESTA SENHA DEVE SER IDÊNTICA às acima!


Dockerfile (parte do comando ENV):
    dockerfile
    Copiar
    ENV PYTHONUNBUFFERED=1 \
        DATABASE_URL=postgresql://homeless_user:SUA_SENHA_FORTE_AQUI@db:5432/homeless_db \
        DEBUG=False


## 3. Construir e Iniciar o Projeto com Docker Compose

Após ajustar as senhas, você pode construir as imagens Docker e iniciar os serviços usando o Docker Compose:

```bash
sudo docker compose build
sudo docker compose up
```

### Estrutura
```
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── server.py             # Ponto de entrada do aplicativo Uvicorn
├── app/
│   ├── __init__.py
│   ├── api.py            # Definições das rotas FastAPI
│   ├── database.py       # Configuração do banco de dados (SQLAlchemy)
│   ├── models.py         # Modelos de dados (SQLAlchemy ORM)
│   └── (outros módulos do seu aplicativo)
├── static/               # Pasta para arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── tests/                # Pasta para seus arquivos de teste
│   └── test_basic.py
└── pytest.ini            # Arquivo de configuração do Pytest para ignorar testes de dependências
```

### Executando Testes

Para executar os testes do seu projeto, utilize o `pytest`. Certifique-se de que o `pytest.ini` esteja configurado para ignorar os testes das dependências, focando apenas nos seus próprios testes.

Para executar os testes a partir da raiz do projeto:

```bash
sudo docker compose run --rm app pytest
