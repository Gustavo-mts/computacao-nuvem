from sqlalchemy import Column, Integer, String, Date, Boolean, Text, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime


class TipoPessoa(enum.Enum):
    FUNCIONARIO = "FUNCIONARIO"
    ACOLHIDO = "ACOLHIDO"


class StatusFuncionario(enum.Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    LICENCA = "LICENCA"


class StatusAcolhimento(enum.Enum):
    ATIVO = "ATIVO"
    TRANSFERIDO = "TRANSFERIDO"
    DESLIGADO = "DESLIGADO"
    EVADIDO = "EVADIDO"


class TurnoEnum(enum.Enum):
    MANHA = "MANHA"
    TARDE = "TARDE"
    NOITE = "NOITE"
    INTEGRAL = "INTEGRAL"


class TipoAbrigo(enum.Enum):
    MASCULINO = "MASCULINO"
    FEMININO = "FEMININO"
    MISTO = "MISTO"
    FAMILIAR = "FAMILIAR"


class Pessoa(Base):
    __tablename__ = "pessoas"
    
    id_pessoa = Column(Integer, primary_key=True, index=True)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    nome = Column(String(200), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone_principal = Column(String(15), nullable=False)
    telefone_secundario = Column(String(15))
    email = Column(String(100), unique=True)
    
    endereco_rua = Column(String(200), nullable=False)
    endereco_numero = Column(String(10))
    endereco_bairro = Column(String(100), nullable=False)
    endereco_cidade = Column(String(100), nullable=False)
    endereco_estado = Column(String(2), nullable=False)
    endereco_cep = Column(String(9))
    
    tipo_pessoa = Column(Enum(TipoPessoa), nullable=False)
    ativo = Column(Boolean, default=True)
    
    funcionario = relationship("Funcionario", back_populates="pessoa", uselist=False)
    acolhido = relationship("Acolhido", back_populates="pessoa", uselist=False)


class Funcionario(Base):
    __tablename__ = "funcionarios"
    
    id_funcionario = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey("pessoas.id_pessoa"), nullable=False, unique=True)
    matricula = Column(String(20), unique=True, nullable=False)
    cargo = Column(String(100), nullable=False)
    data_admissao = Column(Date, nullable=False)
    salario = Column(DECIMAL(10,2), nullable=False)
    turno = Column(Enum(TurnoEnum), nullable=False)
    status_funcionario = Column(Enum(StatusFuncionario), default=StatusFuncionario.ATIVO)
    
    pessoa = relationship("Pessoa", back_populates="funcionario")
    atendimentos = relationship("Atendimento", back_populates="funcionario")


class Acolhido(Base):
    __tablename__ = "acolhidos"
    
    id_acolhido = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey("pessoas.id_pessoa"), nullable=False, unique=True)
    numero_prontuario = Column(String(20), unique=True, nullable=False)
    data_entrada = Column(Date, nullable=False)
    data_saida = Column(Date)
    motivo_acolhimento = Column(Text, nullable=False)
    dependencia_quimica = Column(Boolean, default=False)
    status_acolhimento = Column(Enum(StatusAcolhimento), default=StatusAcolhimento.ATIVO)
    
    pessoa = relationship("Pessoa", back_populates="acolhido")
    familiares = relationship("Familiar", back_populates="acolhido")
    atendimentos = relationship("Atendimento", back_populates="acolhido")
    acolhimentos = relationship("Acolhimento", back_populates="acolhido")


class Abrigo(Base):
    __tablename__ = "abrigos"
    
    id_abrigo = Column(Integer, primary_key=True, index=True)
    cnpj = Column(String(18), unique=True, nullable=False)
    nome = Column(String(200), nullable=False)
    capacidade_total = Column(Integer, nullable=False)
    
    endereco_rua = Column(String(200), nullable=False)
    endereco_numero = Column(String(10))
    endereco_bairro = Column(String(100), nullable=False)
    endereco_cidade = Column(String(100), nullable=False)
    endereco_estado = Column(String(2), nullable=False)
    endereco_cep = Column(String(9))
    
    telefone_principal = Column(String(15), nullable=False)
    tipo_abrigo = Column(Enum(TipoAbrigo), nullable=False)
    responsavel_legal = Column(String(200), nullable=False)
    ativo = Column(Boolean, default=True)
    
    acolhimentos = relationship("Acolhimento", back_populates="abrigo")


class Acolhimento(Base):
    __tablename__ = "acolhimentos"
    
    id_acolhimento = Column(Integer, primary_key=True, index=True)
    id_acolhido = Column(Integer, ForeignKey("acolhidos.id_acolhido"), nullable=False)
    id_abrigo = Column(Integer, ForeignKey("abrigos.id_abrigo"), nullable=False)
    data_entrada = Column(Date, nullable=False)
    data_saida = Column(Date)
    numero_vaga = Column(String(10))
    status_ativo = Column(Boolean, default=True)
    
    acolhido = relationship("Acolhido", back_populates="acolhimentos")
    abrigo = relationship("Abrigo", back_populates="acolhimentos")


class Atendimento(Base):
    __tablename__ = "atendimentos"
    
    id_atendimento = Column(Integer, primary_key=True, index=True)
    id_acolhido = Column(Integer, ForeignKey("acolhidos.id_acolhido"), nullable=False)
    id_funcionario = Column(Integer, ForeignKey("funcionarios.id_funcionario"), nullable=False)
    data_atendimento = Column(Date, nullable=False)
    tipo_atendimento = Column(String(50), nullable=False)
    descricao = Column(Text, nullable=False)
    observacoes = Column(Text)
    
    acolhido = relationship("Acolhido", back_populates="atendimentos")
    funcionario = relationship("Funcionario", back_populates="atendimentos")


class Familiar(Base):
    __tablename__ = "familiares"
    
    id_familiar = Column(Integer, primary_key=True, index=True)
    id_acolhido = Column(Integer, ForeignKey("acolhidos.id_acolhido"), nullable=False)
    nome = Column(String(200), nullable=False)
    parentesco = Column(String(50), nullable=False)
    telefone_principal = Column(String(15), nullable=False)
    contato_emergencia = Column(Boolean, default=False)
    
    acolhido = relationship("Acolhido", back_populates="familiares")