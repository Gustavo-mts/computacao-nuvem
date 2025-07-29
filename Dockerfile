
# Imagem base
FROM python:3.12-slim

# Variável de ambiente para não gerar arquivos pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho no container
WORKDIR /app

# Instala dependências do sistema (psycopg2 precisa do libpq)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependências
COPY requirements.txt .

# Instala dependências Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo o projeto para o container
COPY . .

# Expõe a porta da aplicação
EXPOSE 8000

# Comando padrão para rodar o servidor
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

