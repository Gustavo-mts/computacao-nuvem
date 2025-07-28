# Etapa 1: Usar imagem base do Python
FROM python:3.12-slim

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Instalar dependências do sistema necessárias (PostgreSQL e build)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
# Instala diretamente as dependências listadas.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv jinja2 python-multipart pandas alembic pydantic

# Copiar o restante do projeto para o diretório de trabalho
COPY . /app

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    DATABASE_URL=postgresql://homeless_user:sua_senha_aqui@db:5432/homeless_db \
    DEBUG=False

# Expor a porta padrão do FastAPI
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
