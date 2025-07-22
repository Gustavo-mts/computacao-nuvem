from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Pegando a string de conexão do .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Criando o engine de conexão com o PostgreSQL
engine = create_engine(DATABASE_URL)

# Criando sessão e base para os modelos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()