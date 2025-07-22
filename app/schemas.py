"""
Sistema de Gestão para Abrigos
Schemas de Validação de Dados - Pydantic Models

Este módulo define os schemas de validação para entrada, saída e
processamento de dados do sistema de gestão de abrigos.
Utiliza Pydantic para validação automática e serialização.
"""

from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.models import TipoAbrigo, TurnoEnum, StatusFuncionario, StatusAcolhimento


# Schemas para Gestão de Abrigos
class AbrigoBase(BaseModel):
    """Schema base para dados de abrigo"""
    nome: str
    localizacao: str
    tipo: TipoAbrigo
    capacidade: int


class AbrigoCreate(AbrigoBase):
    """Schema para criação de novo abrigo"""
    cnpj: str
    endereco_rua: str
    endereco_bairro: str
    endereco_cidade: str
    endereco_estado: str
    telefone_principal: str
    responsavel_legal: str


class AbrigoResponse(AbrigoBase):
    """Schema para resposta de dados de abrigo"""
    id_abrigo: int
    cnpj: str
    ativo: bool
    
    class Config:
        from_attributes = True


# Schemas para Gestão de Funcionários
class FuncionarioBase(BaseModel):
    """Schema base para dados de funcionário"""
    nome: str
    cpf: str
    data_nascimento: date
    telefone: str
    cargo: str
    turno: TurnoEnum
    matricula: str


class FuncionarioCreate(FuncionarioBase):
    """Schema para criação de novo funcionário"""
    endereco_rua: str
    endereco_bairro: str
    endereco_cidade: str
    endereco_estado: str
    data_admissao: date
    salario: float
    email: Optional[str] = None


class FuncionarioResponse(FuncionarioBase):
    """Schema para resposta de dados de funcionário"""
    id_funcionario: int
    status_funcionario: StatusFuncionario
    
    class Config:
        from_attributes = True


# Schemas para Profissionais de Saúde
class ProfissionalSaudeBase(BaseModel):
    """Schema base para profissional de saúde"""
    nome: str
    cpf: str
    data_nascimento: date
    telefone: str
    area: str
    registro: str


class ProfissionalSaudeCreate(ProfissionalSaudeBase):
    """Schema para criação de profissional de saúde"""
    endereco_rua: str
    endereco_bairro: str
    endereco_cidade: str
    endereco_estado: str
    email: Optional[str] = None


class ProfissionalSaudeResponse(ProfissionalSaudeBase):
    """Schema para resposta de dados de profissional de saúde"""
    id_funcionario: int
    
    class Config:
        from_attributes = True


# Schemas para Pessoas Acolhidas
class PessoaAcolhidaBase(BaseModel):
    """Schema base para pessoa acolhida"""
    nome: str
    cpf: str
    data_nascimento: date
    historico_saude: Optional[str]
    genero: str
    necessidade_especial: bool


class PessoaAcolhidaCreate(PessoaAcolhidaBase):
    """Schema para criação de pessoa acolhida"""
    telefone_principal: str
    endereco_rua: str
    endereco_bairro: str
    endereco_cidade: str
    endereco_estado: str
    motivo_acolhimento: str
    numero_prontuario: str


class PessoaAcolhidaResponse(PessoaAcolhidaBase):
    """Schema para resposta de dados de pessoa acolhida"""
    id: int
    status_acolhimento: StatusAcolhimento
    
    class Config:
        from_attributes = True


# Schemas para Admissões/Acolhimento
class AdmissaoBase(BaseModel):
    """Schema base para admissão"""
    pessoa_id: int
    abrigo_id: int
    data_admissao: date


class AdmissaoCreate(AdmissaoBase):
    """Schema para criação de nova admissão"""
    numero_vaga: Optional[str] = None


class AdmissaoResponse(AdmissaoBase):
    """Schema para resposta de dados de admissão"""
    id_acolhimento: int
    data_saida: Optional[date] = None
    status_ativo: bool
    
    class Config:
        from_attributes = True


# Schemas para Atendimentos
class AtendimentoBase(BaseModel):
    """Schema base para atendimento"""
    id_acolhido: int
    id_funcionario: int
    data_atendimento: date
    tipo_atendimento: str
    descricao: str


class AtendimentoCreate(AtendimentoBase):
    """Schema para criação de novo atendimento"""
    observacoes: Optional[str] = None


class AtendimentoUpdate(BaseModel):
    """Schema para atualização de atendimento"""
    tipo_atendimento: Optional[str] = None
    descricao: Optional[str] = None
    observacoes: Optional[str] = None


class AtendimentoResponse(AtendimentoBase):
    """Schema para resposta de dados de atendimento"""
    id_atendimento: int
    observacoes: Optional[str] = None
    
    class Config:
        from_attributes = True


# Schemas para Familiares/Contatos
class FamiliarBase(BaseModel):
    """Schema base para familiar/contato"""
    nome: str
    parentesco: str
    telefone_principal: str
    contato_emergencia: bool = False


class FamiliarCreate(FamiliarBase):
    """Schema para criação de familiar/contato"""
    id_acolhido: int


class FamiliarUpdate(BaseModel):
    """Schema para atualização de familiar/contato"""
    nome: Optional[str] = None
    parentesco: Optional[str] = None
    telefone_principal: Optional[str] = None
    contato_emergencia: Optional[bool] = None


class FamiliarResponse(FamiliarBase):
    """Schema para resposta de dados de familiar/contato"""
    id_familiar: int
    id_acolhido: int
    
    class Config:
        from_attributes = True


# Schemas para Pessoas (Genérico)
class PessoaBase(BaseModel):
    """Schema base para pessoa genérica"""
    nome: str
    cpf: str
    data_nascimento: date
    telefone_principal: str
    endereco_rua: str
    endereco_bairro: str
    endereco_cidade: str
    endereco_estado: str


class PessoaCreate(PessoaBase):
    """Schema para criação de pessoa genérica"""
    telefone_secundario: Optional[str] = None
    email: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_cep: Optional[str] = None


class PessoaUpdate(BaseModel):
    """Schema para atualização de pessoa"""
    nome: Optional[str] = None
    telefone_principal: Optional[str] = None
    telefone_secundario: Optional[str] = None
    email: Optional[str] = None
    endereco_rua: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_bairro: Optional[str] = None
    endereco_cidade: Optional[str] = None
    endereco_estado: Optional[str] = None
    endereco_cep: Optional[str] = None


class PessoaResponse(PessoaBase):
    """Schema para resposta de dados de pessoa"""
    id_pessoa: int
    telefone_secundario: Optional[str] = None
    email: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_cep: Optional[str] = None
    tipo_pessoa: str
    ativo: bool
    
    class Config:
        from_attributes = True


# Schemas para Acolhidos (Detalhado)
class AcolhidoBase(BaseModel):
    """Schema base para acolhido detalhado"""
    numero_prontuario: str
    data_entrada: date
    motivo_acolhimento: str


class AcolhidoCreate(AcolhidoBase):
    """Schema para criação de acolhido"""
    id_pessoa: int
    dependencia_quimica: bool = False
    possui_deficiencia: bool = False
    tipo_deficiencia: Optional[str] = None


class AcolhidoUpdate(BaseModel):
    """Schema para atualização de acolhido"""
    numero_prontuario: Optional[str] = None
    motivo_acolhimento: Optional[str] = None
    dependencia_quimica: Optional[bool] = None
    possui_deficiencia: Optional[bool] = None
    tipo_deficiencia: Optional[str] = None
    data_saida: Optional[date] = None
    status_acolhimento: Optional[StatusAcolhimento] = None


class AcolhidoResponse(AcolhidoBase):
    """Schema para resposta de dados de acolhido"""
    id_acolhido: int
    id_pessoa: int
    data_saida: Optional[date] = None
    dependencia_quimica: bool
    possui_deficiencia: bool
    tipo_deficiencia: Optional[str] = None
    status_acolhimento: StatusAcolhimento
    
    class Config:
        from_attributes = True


# Schemas para Acolhimento (Relacionamento)
class AcolhimentoBase(BaseModel):
    """Schema base para acolhimento/hospedagem"""
    id_acolhido: int
    id_abrigo: int
    data_entrada: date


class AcolhimentoCreate(AcolhimentoBase):
    """Schema para criação de acolhimento"""
    numero_vaga: Optional[str] = None


class AcolhimentoUpdate(BaseModel):
    """Schema para atualização de acolhimento"""
    numero_vaga: Optional[str] = None
    data_saida: Optional[date] = None
    status_ativo: Optional[bool] = None


class AcolhimentoResponse(AcolhimentoBase):
    """Schema para resposta de dados de acolhimento"""
    id_acolhimento: int
    data_saida: Optional[date] = None
    numero_vaga: Optional[str] = None
    status_ativo: bool
    
    class Config:
        from_attributes = True


# Schemas de Resposta Complexa (com dados relacionados)
class FuncionarioCompletoResponse(BaseModel):
    """Funcionário com dados completos da pessoa"""
    id_funcionario: int
    matricula: str
    cargo: str
    data_admissao: date
    salario: float
    turno: TurnoEnum
    status_funcionario: StatusFuncionario
    
    # Dados da pessoa
    id_pessoa: int
    nome: str
    cpf: str
    telefone_principal: str
    email: Optional[str] = None
    endereco_completo: str
    
    class Config:
        from_attributes = True


class AcolhidoCompletoResponse(BaseModel):
    """Acolhido com dados completos da pessoa"""
    id_acolhido: int
    numero_prontuario: str
    data_entrada: date
    data_saida: Optional[date] = None
    motivo_acolhimento: str
    status_acolhimento: StatusAcolhimento
    
    # Dados da pessoa
    id_pessoa: int
    nome: str
    cpf: str
    telefone_principal: str
    endereco_completo: str
    
    class Config:
        from_attributes = True


class AdmissaoCompletoResponse(BaseModel):
    """Admissão com dados completos relacionados"""
    id_acolhimento: int
    data_entrada: date
    data_saida: Optional[date] = None
    numero_vaga: Optional[str] = None
    status_ativo: bool
    
    # Dados do acolhido
    acolhido_nome: str
    acolhido_prontuario: str
    
    # Dados do abrigo
    abrigo_nome: str
    abrigo_cidade: str
    
    class Config:
        from_attributes = True


# Schemas de Estatísticas e Relatórios
class EstatisticasSistema(BaseModel):
    """Estatísticas gerais do sistema"""
    total_abrigos: int
    total_funcionarios: int
    total_acolhidos: int
    total_admissoes_ativas: int
    total_atendimentos: int


class EstatisticasAbrigo(BaseModel):
    """Estatísticas específicas de um abrigo"""
    id_abrigo: int
    nome_abrigo: str
    capacidade_total: int
    ocupacao_atual: int
    taxa_ocupacao: float
    total_admissoes_historico: int


# Schemas para Filtros de Busca
class FiltroFuncionario(BaseModel):
    """Filtros para busca de funcionários"""
    nome: Optional[str] = None
    cargo: Optional[str] = None
    turno: Optional[TurnoEnum] = None
    status: Optional[StatusFuncionario] = None
    ativo: bool = True


class FiltroAcolhido(BaseModel):
    """Filtros para busca de acolhidos"""
    nome: Optional[str] = None
    numero_prontuario: Optional[str] = None
    status: Optional[StatusAcolhimento] = None
    data_entrada_inicio: Optional[date] = None
    data_entrada_fim: Optional[date] = None


class FiltroAdmissao(BaseModel):
    """Filtros para busca de admissões"""
    abrigo_id: Optional[int] = None
    status_ativo: Optional[bool] = None
    data_entrada_inicio: Optional[date] = None
    data_entrada_fim: Optional[date] = None


# Schemas de Validação de Dados Únicos
class ValidacaoCPF(BaseModel):
    """Validação de CPF único no sistema"""
    cpf: str
    valido: bool
    existe_sistema: bool = False


class ValidacaoMatricula(BaseModel):
    """Validação de matrícula única no sistema"""
    matricula: str
    valido: bool
    existe_sistema: bool = False


class ValidacaoProntuario(BaseModel):
    """Validação de prontuário único no sistema"""
    numero_prontuario: str
    valido: bool
    existe_sistema: bool = False