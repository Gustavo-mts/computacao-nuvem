#  Sistema de Gestão para Abrigos

Sistema web desenvolvido em Python/FastAPI para gerenciar abrigos e pessoas em situação de vulnerabilidade social.

## Funcionalidades

- **Gestão de Abrigos**: Cadastro, edição e controle de capacidade
- **Gestão de Funcionários**: Controle de equipe com vinculação a abrigos
- **Gestão de Acolhidos**: Cadastro de pessoas em situação de vulnerabilidade
- **Sistema de Admissões**: Controle de entrada e saída nos abrigos
- **Atendimentos**: Registro de atendimentos realizados
- **Relatórios**: Estatísticas e relatórios de ocupação
- **Dashboard**: Visão geral do sistema

## Tecnologias Utilizadas

- **Backend**: Python 3.12, FastAPI, SQLAlchemy
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Banco de Dados**: PostgreSQL
- **Template Engine**: Jinja2

## Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL 12 ou superior
- Git

## Instalação e Configuração

### 1. Clone o repositório

git clone <url-do-repositorio>
cd HomeLess
```
### 2. Crie e ative o ambiente virtual

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate

# Ativar ambiente virtual (Windows)
venv\Scripts\activate
```

### 3. Instale as dependências

pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv jinja2 python-multipart
```

### 4. Configure o banco de dados

#### 4.1 Crie o banco PostgreSQL

-- Conecte no PostgreSQL como superusuário
CREATE DATABASE homeless_db;
CREATE USER homeless_user WITH PASSWORD 'sua_senha_aqui';
GRANT ALL PRIVILEGES ON DATABASE homeless_db TO homeless_user;
```

#### 4.2 Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DATABASE_URL=postgresql://postgres:suasenha@localhost:5432/homeless
DB_HOST=localhost
DB_PORT=5432
DB_NAME=homeless
DB_USER=postgres
DB_PASSWORD=suasenha

### 6. Execute o servidor

python server.py
```

O sistema estará disponível em: `http://localhost:8000`

## 📁 Estrutura do Projeto

```
HomeLess/
├── venv/                    # Ambiente virtual
│   ├── app/                 # Código da aplicação
│   │   ├── api.py          # Rotas da API
│   │   ├── crud.py         # Operações do banco
│   │   ├── database.py     # Configuração do banco
│   │   ├── models.py       # Modelos SQLAlchemy
│   │   └── schemas.py      # Schemas Pydantic
│   ├── templates/          # Templates HTML
│   │   
│   ├── static/             # Arquivos estáticos (CSS, JS)
│   └── server.py           # Arquivo principal
├── .env                    # Variáveis de ambiente
├── requirements.txt              
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





## Solução de Problemas

### Erro de conexão com o banco
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no arquivo `.env`
- Teste a conexão: `psql -U usuario -d banco -h localhost`

### Erro "Template not found"
- Verifique se a pasta `templates/` existe
- Confirme se todos os arquivos HTML estão na pasta
- Reinicie o servidor

### Erro "Column does not exist"
- Execute as migrações do banco de dados
- Verifique se todas as tabelas foram criadas corretamente

### Dependências não encontradas
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt

# Ou instalar individualmente
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv jinja2 python-multipart
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

### Backup do banco
```bash
# Criar backup
pg_dump -U homeless_user -h localhost homeless_db > backup.sql

# Restaurar backup
psql -U homeless_user -h localhost homeless_db < backup.sql
```


### Versão Atual (v1.0)
- CRUD básico de abrigos, funcionários e acolhidos
- Sistema de admissões
- Dashboard com estatísticas
- Interface web responsiva


### Próximas Versões
- Sistema de autenticação
- Relatórios avançados
- API REST completa
- Notificações por email
- Sistema de backup automático
