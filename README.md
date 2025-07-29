Nome do Seu Projeto
Descrição do Projeto
Este é um projeto web desenvolvido com FastAPI em Python, utilizando PostgreSQL como banco de dados. Ele é conteinerizado usando Docker e orquestrado com Docker Compose, facilitando o setup e a execução em qualquer ambiente.

(Sugestão: Adicione uma breve descrição do que o seu projeto faz aqui. Ex: "Este aplicativo tem como objetivo gerenciar informações sobre pessoas em situação de rua, permitindo o registro, consulta e atualização de dados relevantes.")

Funcionalidades
API RESTful: Construído com FastAPI para uma comunicação eficiente e estruturada.

Persistência de Dados: Utiliza PostgreSQL para armazenamento seguro e escalável de informações.

Containerização: Empacotado com Docker para garantir consistência em diferentes ambientes.

Orquestração Simples: Gerenciado via Docker Compose para fácil inicialização e gerenciamento de serviços (aplicativo e banco de dados).

Serviço de Arquivos Estáticos: Configurado para servir arquivos CSS, JavaScript e imagens a partir de uma pasta static.

Pré-requisitos
Antes de iniciar o projeto, certifique-se de ter as seguintes ferramentas instaladas em sua máquina:

Docker: Instalação do Docker

Docker Compose: Geralmente vem junto com a instalação do Docker Desktop. Caso contrário, siga as instruções de instalação do Docker Compose.

Primeiros Passos
Siga estas instruções para configurar e executar o projeto em sua máquina local.

1. Clonar o Repositório
Primeiro, clone este repositório para o seu ambiente local:

git clone https://github.com/Gustavo-mts/computacao-nuvem.git
cd seu-repositorio

2. Configuração das Variáveis de Ambiente
O projeto utiliza variáveis de ambiente para a configuração do banco de dados e outros parâmetros. As variáveis estão definidas no compose.yaml e no Dockerfile.

ATENÇÃO: No seu compose.yaml e Dockerfile, a senha do banco de dados está definida como sua_senha_aqui. Para fins de segurança e para que o banco de dados funcione corretamente, você DEVE substituir sua_senha_aqui por uma senha forte e real em ambos os arquivos.

compose.yaml (parte do serviço db e app):

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

ENV PYTHONUNBUFFERED=1 \
    DATABASE_URL=postgresql://homeless_user:SUA_SENHA_FORTE_AQUI@db:5432/homeless_db \
    DEBUG=False

3. Construir e Iniciar o Projeto com Docker Compose
Após ajustar as senhas, você pode construir as imagens Docker e iniciar os serviços usando o Docker Compose:

sudo docker compose build
sudo docker compose up

Este comando irá:

Construir a imagem Docker para o seu aplicativo (app).

Puxar a imagem do PostgreSQL (db).

Iniciar ambos os contêineres.

O aplicativo estará disponível em http://localhost:8000.

Estrutura do Projeto
A estrutura básica do seu projeto deve ser algo parecido com isto:

.
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── server.py             # Ponto de entrada do aplicativo Uvicorn
├── app/
│   ├── _init_.py
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

Desenvolvimento
Executando Testes
Para executar os testes do seu projeto, utilize o pytest. Certifique-se de que o pytest.ini esteja configurado para ignorar os testes das dependências, focando apenas nos seus próprios testes.

Para executar os testes a partir da raiz do projeto:

sudo docker compose run --rm app pytest

Ou, se você tem uma pasta tests/ para seus testes:

sudo docker compose run --rm app pytest tests/

CI/CD (Integração e Entrega Contínua)
Este projeto está configurado para utilizar GitHub Actions para CI/CD. O workflow está definido no arquivo .github/workflows/main.yml e inclui os seguintes passos:

Lint do Código: Verifica a qualidade do código com flake8.

Execução de Testes: Roda os testes configurados com pytest.

Build da Imagem Docker: Constrói a imagem Docker do aplicativo.

Push da Imagem Docker: Envia a imagem construída para o GitHub Container Registry (ghcr.io).

O workflow é disparado automaticamente em cada push para a branch main e em cada Pull Request.

Como Contribuir
Ficou interessado em contribuir? Ótimo! Sinta-se à vontade para:

Fazer um fork deste repositório.

Criar uma branch para sua funcionalidade ou correção (git checkout -b feature/minha-nova-funcionalidade).

Fazer suas alterações e commitá-las (git commit -m 'feat: adiciona nova funcionalidade X').

Fazer push para a sua branch (git push origin feature/minha-nova-funcionalidade).

Abrir um Pull Request.

Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
