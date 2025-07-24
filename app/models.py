from sqlalchemy import Column, Integer, String, Date, Boolean, Text, ForeignKey, Enum, DECIMAL, DateTime
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
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    funcionario = relationship("Funcionario", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")
    acolhido = relationship("Acolhido", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Pessoa(id={self.id_pessoa}, nome='{self.nome}', cpf='{self.cpf}')>"
    
    @property
    def endereco_completo(self):
        """Retorna o endereço completo formatado"""
        endereco = f"{self.endereco_rua}"
        if self.endereco_numero:
            endereco += f", {self.endereco_numero}"
        endereco += f", {self.endereco_bairro}, {self.endereco_cidade}/{self.endereco_estado}"
        if self.endereco_cep:
            endereco += f" - CEP: {self.endereco_cep}"
        return endereco


class Abrigo(Base):
    __tablename__ = "abrigos"
    
    id_abrigo = Column(Integer, primary_key=True, index=True)
    cnpj = Column(String(18), unique=True, nullable=False, index=True)
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
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    funcionarios = relationship("Funcionario", back_populates="abrigo")
    acolhimentos = relationship("Acolhimento", back_populates="abrigo")
    
    def __repr__(self):
        return f"<Abrigo(id={self.id_abrigo}, nome='{self.nome}', cnpj='{self.cnpj}')>"
    
    @property
    def endereco_completo(self):
        """Retorna o endereço completo formatado"""
        endereco = f"{self.endereco_rua}"
        if self.endereco_numero:
            endereco += f", {self.endereco_numero}"
        endereco += f", {self.endereco_bairro}, {self.endereco_cidade}/{self.endereco_estado}"
        if self.endereco_cep:
            endereco += f" - CEP: {self.endereco_cep}"
        return endereco
    
    @property
    def ocupacao_atual(self):
        """Retorna a ocupação atual do abrigo"""
        return len([a for a in self.acolhimentos if a.status_ativo])
    
    @property
    def vagas_disponiveis(self):
        """Retorna o número de vagas disponíveis"""
        return self.capacidade_total - self.ocupacao_atual
    
    @property
    def taxa_ocupacao(self):
        """Retorna a taxa de ocupação em percentual"""
        if self.capacidade_total == 0:
            return 0
        return (self.ocupacao_atual / self.capacidade_total) * 100
    
    @property
    def total_funcionarios(self):
        """Retorna o total de funcionários ativos no abrigo"""
        return len([f for f in self.funcionarios if f.status_funcionario == StatusFuncionario.ATIVO])


class Funcionario(Base):
    __tablename__ = "funcionarios"
    
    id_funcionario = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey("pessoas.id_pessoa"), nullable=False, unique=True)
    id_abrigo = Column(Integer, ForeignKey("abrigos.id_abrigo"), nullable=True, index=True)
    matricula = Column(String(20), unique=True, nullable=False, index=True)
    cargo = Column(String(100), nullable=False)
    data_admissao = Column(Date, nullable=False)
    salario = Column(DECIMAL(10,2), nullable=False)
    turno = Column(Enum(TurnoEnum), nullable=False)
    status_funcionario = Column(Enum(StatusFuncionario), default=StatusFuncionario.ATIVO, index=True)
    
    # Relacionamentos
    pessoa = relationship("Pessoa", back_populates="funcionario")
    abrigo = relationship("Abrigo", back_populates="funcionarios")
    atendimentos = relationship("Atendimento", back_populates="funcionario")
    
    def __repr__(self):
        return f"<Funcionario(id={self.id_funcionario}, matricula='{self.matricula}', nome='{self.pessoa.nome if self.pessoa else 'N/A'}')>"
    
    @property
    def nome(self):
        """Retorna o nome da pessoa"""
        return self.pessoa.nome if self.pessoa else None
    
    @property
    def tempo_servico_dias(self):
        """Retorna o tempo de serviço em dias"""
        from datetime import date
        return (date.today() - self.data_admissao).days
    
    @property
    def tempo_servico_formatado(self):
        """Retorna o tempo de serviço formatado"""
        dias = self.tempo_servico_dias
        if dias < 30:
            return f"{dias} dias"
        elif dias < 365:
            meses = dias // 30
            return f"{meses} meses"
        else:
            anos = dias // 365
            return f"{anos} anos"
    
    @property
    def total_atendimentos(self):
        """Retorna o total de atendimentos realizados"""
        return len(self.atendimentos)


class Acolhido(Base):
    __tablename__ = "acolhidos"
    
    id_acolhido = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey("pessoas.id_pessoa"), nullable=False, unique=True)
    numero_prontuario = Column(String(20), unique=True, nullable=False, index=True)
    data_entrada = Column(Date, nullable=False)
    data_saida = Column(Date)
    motivo_acolhimento = Column(Text, nullable=False)
    dependencia_quimica = Column(Boolean, default=False)
    possui_deficiencia = Column(Boolean, default=False)
    tipo_deficiencia = Column(String(200))
    status_acolhimento = Column(Enum(StatusAcolhimento), default=StatusAcolhimento.ATIVO, index=True)
    
    # Relacionamentos
    pessoa = relationship("Pessoa", back_populates="acolhido")
    familiares = relationship("Familiar", back_populates="acolhido", cascade="all, delete-orphan")
    atendimentos = relationship("Atendimento", back_populates="acolhido")
    acolhimentos = relationship("Acolhimento", back_populates="acolhido")
    
    def __repr__(self):
        return f"<Acolhido(id={self.id_acolhido}, prontuario='{self.numero_prontuario}', nome='{self.pessoa.nome if self.pessoa else 'N/A'}')>"
    
    @property
    def nome(self):
        """Retorna o nome da pessoa"""
        return self.pessoa.nome if self.pessoa else None
    
    @property
    def admissao_ativa(self):
        """Retorna a admissão ativa atual, se houver"""
        return next((a for a in self.acolhimentos if a.status_ativo), None)
    
    @property
    def tempo_acolhimento_dias(self):
        """Retorna o tempo de acolhimento em dias"""
        from datetime import date
        if self.data_saida:
            return (self.data_saida - self.data_entrada).days
        return (date.today() - self.data_entrada).days
    
    @property
    def tempo_acolhimento_formatado(self):
        """Retorna o tempo de acolhimento formatado"""
        dias = self.tempo_acolhimento_dias
        if dias < 30:
            return f"{dias} dias"
        elif dias < 365:
            meses = dias // 30
            return f"{meses} meses"
        else:
            anos = dias // 365
            return f"{anos} anos"
    
    @property
    def total_atendimentos(self):
        """Retorna o total de atendimentos recebidos"""
        return len(self.atendimentos)
    
    @property
    def contatos_emergencia(self):
        """Retorna os familiares marcados como contato de emergência"""
        return [f for f in self.familiares if f.contato_emergencia]


class Acolhimento(Base):
    __tablename__ = "acolhimentos"
    
    id_acolhimento = Column(Integer, primary_key=True, index=True)
    id_acolhido = Column(Integer, ForeignKey("acolhidos.id_acolhido"), nullable=False, index=True)
    id_abrigo = Column(Integer, ForeignKey("abrigos.id_abrigo"), nullable=False, index=True)
    data_entrada = Column(Date, nullable=False)
    data_saida = Column(Date)
    numero_vaga = Column(String(10))
    status_ativo = Column(Boolean, default=True, index=True)
    motivo_saida = Column(String(100))
    observacoes_saida = Column(Text)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    acolhido = relationship("Acolhido", back_populates="acolhimentos")
    abrigo = relationship("Abrigo", back_populates="acolhimentos")
    
    def __repr__(self):
        return f"<Acolhimento(id={self.id_acolhimento}, acolhido='{self.acolhido.nome if self.acolhido else 'N/A'}', abrigo='{self.abrigo.nome if self.abrigo else 'N/A'}')>"
    
    @property
    def tempo_permanencia_dias(self):
        """Retorna o tempo de permanência em dias"""
        from datetime import date
        data_fim = self.data_saida if self.data_saida else date.today()
        return (data_fim - self.data_entrada).days
    
    @property
    def tempo_permanencia_formatado(self):
        """Retorna o tempo de permanência formatado"""
        dias = self.tempo_permanencia_dias
        if dias == 0:
            return "Hoje"
        elif dias == 1:
            return "1 dia"
        elif dias < 30:
            return f"{dias} dias"
        elif dias < 365:
            meses = dias // 30
            return f"{meses} meses"
        else:
            anos = dias // 365
            return f"{anos} anos"


class Atendimento(Base):
    __tablename__ = "atendimentos"
    
    id_atendimento = Column(Integer, primary_key=True, index=True)
    id_acolhido = Column(Integer, ForeignKey("acolhidos.id_acolhido"), nullable=False, index=True)
    id_funcionario = Column(Integer, ForeignKey("funcionarios.id_funcionario"), nullable=False, index=True)
    data_atendimento = Column(Date, nullable=False, index=True)
    tipo_atendimento = Column(String(50), nullable=False)
    descricao = Column(Text, nullable=False)
    observacoes = Column(Text)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    acolhido = relationship("Acolhido", back_populates="atendimentos")
    funcionario = relationship("Funcionario", back_populates="atendimentos")
    
    def __repr__(self):
        return f"<Atendimento(id={self.id_atendimento}, tipo='{self.tipo_atendimento}', data='{self.data_atendimento}')>"


class Familiar(Base):
    __tablename__ = "familiares"
    
    id_familiar = Column(Integer, primary_key=True, index=True)
    id_acolhido = Column(Integer, ForeignKey("acolhidos.id_acolhido"), nullable=False, index=True)
    nome = Column(String(200), nullable=False)
    parentesco = Column(String(50), nullable=False)
    telefone_principal = Column(String(15), nullable=False)
    telefone_secundario = Column(String(15))
    email = Column(String(100))
    endereco = Column(String(500))
    contato_emergencia = Column(Boolean, default=False, index=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    acolhido = relationship("Acolhido", back_populates="familiares")
    
    def __repr__(self):
        return f"<Familiar(id={self.id_familiar}, nome='{self.nome}', parentesco='{self.parentesco}')>"


# ========================= TABELAS AUXILIARES =========================

class HistoricoTransferencia(Base):
    """Histórico de transferências de funcionários entre abrigos"""
    __tablename__ = "historico_transferencias"
    
    id_transferencia = Column(Integer, primary_key=True, index=True)
    id_funcionario = Column(Integer, ForeignKey("funcionarios.id_funcionario"), nullable=False)
    id_abrigo_origem = Column(Integer, ForeignKey("abrigos.id_abrigo"))
    id_abrigo_destino = Column(Integer, ForeignKey("abrigos.id_abrigo"))
    data_transferencia = Column(DateTime, default=datetime.utcnow)
    motivo = Column(String(200))
    observacoes = Column(Text)
    
    # Relacionamentos
    funcionario = relationship("Funcionario")
    abrigo_origem = relationship("Abrigo", foreign_keys=[id_abrigo_origem])
    abrigo_destino = relationship("Abrigo", foreign_keys=[id_abrigo_destino])


class LogSistema(Base):
    """Log de ações importantes do sistema"""
    __tablename__ = "logs_sistema"
    
    id_log = Column(Integer, primary_key=True, index=True)
    tabela = Column(String(50), nullable=False)
    id_registro = Column(Integer, nullable=False)
    acao = Column(String(20), nullable=False)  # CREATE, UPDATE, DELETE
    dados_anteriores = Column(Text)  # JSON dos dados antes da alteração
    dados_novos = Column(Text)  # JSON dos dados após a alteração
    usuario = Column(String(100))  # Para futuro sistema de autenticação
    data_acao = Column(DateTime, default=datetime.utcnow, index=True)
    ip_origem = Column(String(45))
    
    def __repr__(self):
        return f"<LogSistema(id={self.id_log}, tabela='{self.tabela}', acao='{self.acao}')>"


# ========================= VIEWS MATERIALIZADAS (FUTURO) =========================

class ViewEstatisticasAbrigo(Base):
    """View materializada para estatísticas de abrigos"""
    __tablename__ = "view_estatisticas_abrigos"
    
    id_abrigo = Column(Integer, primary_key=True)
    nome_abrigo = Column(String(200))
    capacidade_total = Column(Integer)
    ocupacao_atual = Column(Integer)
    taxa_ocupacao = Column(DECIMAL(5,2))
    total_funcionarios = Column(Integer)
    total_admissoes_historico = Column(Integer)
    ultima_atualizacao = Column(DateTime)
    
    def __repr__(self):
        return f"<ViewEstatisticasAbrigo(abrigo='{self.nome_abrigo}', ocupacao={self.taxa_ocupacao}%)>"