# Sistema de Gestão para Abrigos

Sistema web desenvolvido em Python/FastAPI para gerenciar abrigos e pessoas em situação de vulnerabilidade social.

## Funcionalidades

- **Gestão de Abrigos**: Cadastro, edição e controle de capacidade
- **Gestão de Funcionários**: Controle de equipe com vinculação a abrigos
- **Gestão de Acolhidos**: Cadastro de pessoas em situação de vulnerabilidade
- **Sistema de Admissões**: Controle de entrada e saída nos abrigos
- **Atendimentos**: Registro de atendimentos realizados
- **Relatórios**: Estatísticas e relatórios de ocupação
- **Dashboard**: Visão geral do sistema

## 🛠Tecnologias Utilizadas

- **Backend**: Python 3.12, FastAPI, SQLAlchemy
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Banco de Dados**: PostgreSQL
- **Template Engine**: Jinja2

## Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL 12 ou superior
- Git

## 🚀 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd HomeLess
```

### 2. Crie e ative o ambiente virtual
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate

# Ativar ambiente virtual (Windows)
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
# Opção 1: Usando requirements.txt (recomendado)
pip install -r requirements.txt

# Opção 2: Instalação manual
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv jinja2 python-multipart pandas alembic pydantic
```

### 4. Configure o banco de dados

#### 4.1 Crie o banco PostgreSQL
```sql
-- Conecte no PostgreSQL como superusuário
CREATE DATABASE homeless_db;
CREATE USER homeless_user WITH PASSWORD 'sua_senha_aqui';
GRANT ALL PRIVILEGES ON DATABASE homeless_db TO homeless_user;
```

#### 4.2 Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
# Configuração do Banco de Dados
DATABASE_URL=postgresql://homeless_user:sua_senha_aqui@localhost:5432/homeless_db

# Configurações Alternativas (opcional)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=homeless_db
DB_USER=homeless_user
DB_PASSWORD=sua_senha_aqui

# Configurações da Aplicação
DEBUG=True
SECRET_KEY=sua_chave_secreta_aqui
```

### 5. Execute as migrações do banco
```bash
# Conecte no PostgreSQL e execute as migrações necessárias
psql -U homeless_user -d homeless_db

# Execute o script de migração (Quando disponível na documentação)
```

### 6. Execute o servidor
```bash
python server.py
```

O sistema estará disponível em: `http://localhost:8000`

## 📄 Arquivo requirements.txt

Crie o arquivo `requirements.txt` com as seguintes dependências:

```text
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.7
alembic==1.12.1
python-dotenv==1.0.0
pydantic==2.5.0
pandas==2.1.4
jinja2==3.1.2
python-multipart==0.0.6
```

## 📁 Estrutura do Projeto

```
HomeLess/
├── app/                     # Código da aplicação
│   ├── __init__.py
│   ├── api.py              # Rotas da API
│   ├── crud.py             # Operações do banco
│   ├── database.py         # Configuração do banco
│   ├── models.py           # Modelos SQLAlchemy
│   └── schemas.py          # Schemas Pydantic
├── templates/              # Templates HTML
│   ├── base.html
│   ├── dashboard.html
│   ├── abrigos.html
│   ├── funcionarios.html
│   └── ...
├── static/                 # Arquivos estáticos (CSS, JS)
├── venv/                   # Ambiente virtual
├── .env                    # Variáveis de ambiente
├── requirements.txt        # Dependências do projeto
├── server.py              # Arquivo principal
└── README.md              # Este arquivo
```

## Como Usar

### Dashboard
- Acesse `http://localhost:8000` para ver o painel principal
- Visualize estatísticas gerais do sistema

### Cadastrar Abrigo
1. Navegue para "Abrigos" → "Novo Abrigo"
2. Preencha os dados do abrigo
3. Defina capacidade e tipo do abrigo

### Cadastrar Funcionário
1. Vá em "Funcionários" → "Novo Funcionário"
2. Preencha dados pessoais e profissionais
3. Opcionalmente vincule a um abrigo

### Cadastrar Pessoa Acolhida
1. Acesse "Nova Pessoa"
2. Preencha dados pessoais e motivo do acolhimento
3. Defina número do prontuário

### Registrar Admissão
1. Vá em "Admissões" → "Nova Admissão"
2. Selecione a pessoa e o abrigo
3. Defina data e número da vaga

## 🔧 Configurações Avançadas

### Migrações do Banco de Dados (Quando disponível)

Execute as seguintes queries no PostgreSQL para configurar o banco():

```sql
-- Adicionar colunas de auditoria
ALTER TABLE pessoas ADD COLUMN IF NOT EXISTS data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE pessoas ADD COLUMN IF NOT EXISTS data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE abrigos ADD COLUMN IF NOT EXISTS data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE abrigos ADD COLUMN IF NOT EXISTS data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Adicionar relacionamento funcionário-abrigo
ALTER TABLE funcionarios ADD COLUMN IF NOT EXISTS id_abrigo INTEGER;
ALTER TABLE funcionarios ADD CONSTRAINT fk_funcionario_abrigo 
    FOREIGN KEY (id_abrigo) REFERENCES abrigos(id_abrigo) ON DELETE SET NULL;

-- Criar índices para performance
CREATE INDEX IF NOT EXISTS idx_funcionarios_abrigo ON funcionarios(id_abrigo);
CREATE INDEX IF NOT EXISTS idx_pessoas_ativo ON pessoas(ativo);
CREATE INDEX IF NOT EXISTS idx_abrigos_ativo ON abrigos(ativo);
```

## Solução de Problemas

### Erro de conexão com o banco
- Verifique se o PostgreSQL está rodando: `sudo systemctl status postgresql`
- Confirme as credenciais no arquivo `.env`
- Teste a conexão: `psql -U homeless_user -d homeless_db -h localhost`

### Erro "Template not found"
- Verifique se a pasta `templates/` existe na raiz do projeto
- Confirme se todos os arquivos HTML estão na pasta
- Reinicie o servidor com `python server.py`

### Erro "Column does not exist"
- Execute as migrações do banco de dados (seção Configurações Avançadas)
- Verifique se todas as tabelas foram criadas corretamente
- Confirme a versão do PostgreSQL (mínimo 12)

### Dependências não encontradas
```bash
# Atualizar pip
pip install --upgrade pip

# Reinstalar dependências
pip install --upgrade -r requirements.txt

# Verificar instalação
pip list
```

### Problemas com psycopg2
```bash
# Ubuntu/Debian
sudo apt-get install libpq-dev python3-dev

# CentOS/RHEL
sudo yum install postgresql-devel python3-devel

# Reinstalar psycopg2
pip uninstall psycopg2-binary
pip install psycopg2-binary
```

## Scripts Úteis

### Criar dados de teste
```python
# Execute no console Python com o ambiente ativo
from app.database import SessionLocal
from app import crud, schemas
from app.models import TipoAbrigo, TurnoEnum
from datetime import date

db = SessionLocal()

# Criar abrigo de teste
abrigo_data = schemas.AbrigoCreate(
    nome="Abrigo Teste",
    tipo=TipoAbrigo.MISTO,
    capacidade=50,
    cnpj="12.345.678/0001-90",
    endereco_rua="Rua Teste, 123",
    endereco_bairro="Centro",
    endereco_cidade="Quixadá",
    endereco_estado="CE",
    telefone_principal="(85) 99999-9999",
    responsavel_legal="Administrador Teste"
)
crud.criar_abrigo(db, abrigo_data)
```

### Backup e Restore do banco
```bash
# Criar backup
pg_dump -U homeless_user -h localhost homeless_db > backup_$(date +%Y%m%d).sql

# Restaurar backup
psql -U homeless_user -h localhost homeless_db < backup_20240101.sql

# Backup compactado
pg_dump -U homeless_user -h localhost homeless_db | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Verificar status do sistema
```bash
# Verificar portas em uso
netstat -tulpn | grep :8000

# Logs do PostgreSQL (Ubuntu)
sudo tail -f /var/log/postgresql/postgresql-*.log

# Verificar espaço em disco
df -h
du -sh HomeLess/
```

## Roadmap

### Versão Atual (v1.0)
- CRUD básico de abrigos, funcionários e acolhidos
- Sistema de admissões
- Dashboard com estatísticas
- Interface web responsiva
---
