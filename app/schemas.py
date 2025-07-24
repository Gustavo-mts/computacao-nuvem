from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from app.models import TipoAbrigo, TurnoEnum, StatusFuncionario, StatusAcolhimento


# ========================= PESSOA BASE =========================

class PessoaBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    telefone_principal: str
    endereco_rua: str
    endereco_bairro: str
    endereco_cidade: str
    endereco_estado: str


class PessoaCreate(PessoaBase):
    telefone_secundario: Optional[str] = None
    email: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_cep: Optional[str] = None


class PessoaUpdate(BaseModel):
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
    id_pessoa: int
    telefone_secundario: Optional[str] = None
    email: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_cep: Optional[str] = None
    tipo_pessoa: str
    ativo: bool
    
    class Config:
        from_attributes = True


# ========================= ABRIGO =========================

class AbrigoBase(BaseModel):
    nome: str
    tipo: TipoAbrigo
    capacidade: int


class AbrigoCreate(AbrigoBase):
    cnpj: str
    endereco_rua: str
    endereco_bairro: str
    endereco_cidade: str
    endereco_estado: str
    telefone_principal: str
    responsavel_legal: str
    endereco_numero: Optional[str] = None
    endereco_cep: Optional[str] = None


class AbrigoUpdate(BaseModel):
    nome: Optional[str] = None
    capacidade: Optional[int] = None
    endereco_rua: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_bairro: Optional[str] = None
    endereco_cidade: Optional[str] = None
    endereco_estado: Optional[str] = None
    endereco_cep: Optional[str] = None
    telefone_principal: Optional[str] = None
    tipo: Optional[TipoAbrigo] = None
    responsavel_legal: Optional[str] = None
    ativo: Optional[bool] = None


class AbrigoResponse(AbrigoBase):
    id_abrigo: int
    cnpj: str
    endereco_rua: str
    endereco_bairro: str
    endereco_cidade: str
    endereco_estado: str
    telefone_principal: str
    responsavel_legal: str
    ativo: bool
    endereco_numero: Optional[str] = None
    endereco_cep: Optional[str] = None
    
    class Config:
        from_attributes = True


# ========================= FUNCIONÁRIO =========================

class FuncionarioBase(BaseModel):
    matricula: str
    cargo: str
    turno: TurnoEnum
    salario: float


class FuncionarioCreate(PessoaCreate):
    matricula: str
    cargo: str
    turno: TurnoEnum
    salario: float
    data_admissao: date
    id_abrigo: Optional[int] = None


class FuncionarioUpdate(BaseModel):
    # Dados pessoais
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
    
    # Dados funcionais
    cargo: Optional[str] = None
    salario: Optional[float] = None
    turno: Optional[TurnoEnum] = None
    status_funcionario: Optional[StatusFuncionario] = None
    id_abrigo: Optional[int] = None


class FuncionarioResponse(FuncionarioBase):
    id_funcionario: int
    id_pessoa: int
    id_abrigo: Optional[int] = None
    data_admissao: date
    status_funcionario: StatusFuncionario
    
    # Dados da pessoa
    nome: str
    cpf: str
    data_nascimento: date
    telefone_principal: str
    telefone_secundario: Optional[str] = None
    email: Optional[str] = None
    endereco_rua: str
    endereco_numero: Optional[str] = None
    endereco_bairro: str
    endereco_cidade: str
    endereco_estado: str
    endereco_cep: Optional[str] = None
    
    class Config:
        from_attributes = True


class FuncionarioCompletoResponse(BaseModel):
    id_funcionario: int
    matricula: str
    cargo: str
    data_admissao: date
    salario: float
    turno: TurnoEnum
    status_funcionario: StatusFuncionario
    id_abrigo: Optional[int] = None
    
    id_pessoa: int
    nome: str
    cpf: str
    telefone_principal: str
    email: Optional[str] = None
    endereco_completo: str
    
    # Dados do abrigo (se vinculado)
    abrigo_nome: Optional[str] = None
    abrigo_cidade: Optional[str] = None
    
    class Config:
        from_attributes = True


# ========================= PROFISSIONAL DE SAÚDE =========================

class ProfissionalSaudeBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    telefone: str
    area: str
    registro: str


class ProfissionalSaudeCreate(ProfissionalSaudeBase):
    endereco_rua: str
    endereco_bairro: str
    endereco_cidade: str
    endereco_estado: str
    endereco_numero: Optional[str] = None
    endereco_cep: Optional[str] = None
    email: Optional[str] = None
    telefone_secundario: Optional[str] = None


class ProfissionalSaudeResponse(ProfissionalSaudeBase):
    id_funcionario: int
    
    class Config:
        from_attributes = True


# ========================= ACOLHIDO =========================

class AcolhidoBase(BaseModel):
    numero_prontuario: str
    data_entrada: date
    motivo_acolhimento: str


class AcolhidoCreate(PessoaCreate):
    numero_prontuario: str
    motivo_acolhimento: str
    dependencia_quimica: bool = False
    possui_deficiencia: bool = False
    tipo_deficiencia: Optional[str] = None


class AcolhidoUpdate(BaseModel):
    numero_prontuario: Optional[str] = None
    motivo_acolhimento: Optional[str] = None
    dependencia_quimica: Optional[bool] = None
    possui_deficiencia: Optional[bool] = None
    tipo_deficiencia: Optional[str] = None
    data_saida: Optional[date] = None
    status_acolhimento: Optional[StatusAcolhimento] = None


class AcolhidoResponse(AcolhidoBase):
    id_acolhido: int
    id_pessoa: int
    data_saida: Optional[date] = None
    dependencia_quimica: bool
    possui_deficiencia: bool
    tipo_deficiencia: Optional[str] = None
    status_acolhimento: StatusAcolhimento
    
    # Dados da pessoa
    nome: str
    cpf: str
    data_nascimento: date
    telefone_principal: str
    endereco_completo: str
    
    class Config:
        from_attributes = True


class AcolhidoCompletoResponse(BaseModel):
    id_acolhido: int
    numero_prontuario: str
    data_entrada: date
    data_saida: Optional[date] = None
    motivo_acolhimento: str
    status_acolhimento: StatusAcolhimento
    dependencia_quimica: bool
    possui_deficiencia: bool
    tipo_deficiencia: Optional[str] = None
    
    id_pessoa: int
    nome: str
    cpf: str
    telefone_principal: str
    endereco_completo: str
    
    class Config:
        from_attributes = True


# ========================= PESSOA ACOLHIDA (LEGACY) =========================

class PessoaAcolhidaBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    historico_saude: Optional[str] = None
    genero: str
    necessidade_especial: bool = False


class PessoaAcolhidaCreate(PessoaAcolhidaBase):
    telefone_principal: str
    endereco_rua: str
    endereco_bairro: str
    endereco_cidade: str
    endereco_estado: str
    motivo_acolhimento: str
    numero_prontuario: str
    telefone_secundario: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_cep: Optional[str] = None


class PessoaAcolhidaResponse(PessoaAcolhidaBase):
    id: int
    status_acolhimento: StatusAcolhimento
    
    class Config:
        from_attributes = True


# ========================= ACOLHIMENTO/ADMISSÃO =========================

class AcolhimentoBase(BaseModel):
    id_acolhido: int
    id_abrigo: int
    data_entrada: date


class AcolhimentoCreate(AcolhimentoBase):
    numero_vaga: Optional[str] = None


class AcolhimentoUpdate(BaseModel):
    numero_vaga: Optional[str] = None
    data_saida: Optional[date] = None
    status_ativo: Optional[bool] = None
    motivo_saida: Optional[str] = None
    observacoes_saida: Optional[str] = None


class AcolhimentoResponse(AcolhimentoBase):
    id_acolhimento: int
    data_saida: Optional[date] = None
    numero_vaga: Optional[str] = None
    status_ativo: bool
    motivo_saida: Optional[str] = None
    observacoes_saida: Optional[str] = None
    
    class Config:
        from_attributes = True


# Aliases para compatibilidade
AdmissaoBase = AcolhimentoBase
AdmissaoCreate = AcolhimentoCreate
AdmissaoUpdate = AcolhimentoUpdate
AdmissaoResponse = AcolhimentoResponse


class AdmissaoCompletoResponse(BaseModel):
    id_acolhimento: int
    data_entrada: date
    data_saida: Optional[date] = None
    numero_vaga: Optional[str] = None
    status_ativo: bool
    
    acolhido_nome: str
    acolhido_prontuario: str
    
    abrigo_nome: str
    abrigo_cidade: str
    
    class Config:
        from_attributes = True


# ========================= ATENDIMENTO =========================

class AtendimentoBase(BaseModel):
    id_acolhido: int
    id_funcionario: int
    data_atendimento: date
    tipo_atendimento: str
    descricao: str


class AtendimentoCreate(AtendimentoBase):
    observacoes: Optional[str] = None


class AtendimentoUpdate(BaseModel):
    tipo_atendimento: Optional[str] = None
    descricao: Optional[str] = None
    observacoes: Optional[str] = None


class AtendimentoResponse(AtendimentoBase):
    id_atendimento: int
    observacoes: Optional[str] = None
    
    class Config:
        from_attributes = True


# ========================= FAMILIAR =========================

class FamiliarBase(BaseModel):
    nome: str
    parentesco: str
    telefone_principal: str
    contato_emergencia: bool = False


class FamiliarCreate(FamiliarBase):
    id_acolhido: int
    telefone_secundario: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None


class FamiliarUpdate(BaseModel):
    nome: Optional[str] = None
    parentesco: Optional[str] = None
    telefone_principal: Optional[str] = None
    telefone_secundario: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    contato_emergencia: Optional[bool] = None


class FamiliarResponse(FamiliarBase):
    id_familiar: int
    id_acolhido: int
    telefone_secundario: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    
    class Config:
        from_attributes = True


# ========================= ESTATÍSTICAS =========================

class EstatisticasSistema(BaseModel):
    total_abrigos: int
    total_funcionarios: int
    total_acolhidos: int
    total_admissoes_ativas: int
    total_atendimentos: int


class EstatisticasAbrigo(BaseModel):
    id_abrigo: int
    nome_abrigo: str
    capacidade_total: int
    ocupacao_atual: int
    taxa_ocupacao: float
    total_funcionarios: int
    total_admissoes_historico: int


# ========================= FILTROS =========================

class FiltroFuncionario(BaseModel):
    nome: Optional[str] = None
    cargo: Optional[str] = None
    turno: Optional[TurnoEnum] = None
    status: Optional[StatusFuncionario] = None
    abrigo_id: Optional[int] = None
    ativo: bool = True


class FiltroAcolhido(BaseModel):
    nome: Optional[str] = None
    numero_prontuario: Optional[str] = None
    status: Optional[StatusAcolhimento] = None
    data_entrada_inicio: Optional[date] = None
    data_entrada_fim: Optional[date] = None
    abrigo_id: Optional[int] = None


class FiltroAdmissao(BaseModel):
    abrigo_id: Optional[int] = None
    status_ativo: Optional[bool] = None
    data_entrada_inicio: Optional[date] = None
    data_entrada_fim: Optional[date] = None


class FiltroAbrigo(BaseModel):
    nome: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    tipo: Optional[TipoAbrigo] = None
    ativo: bool = True


# ========================= VALIDAÇÕES =========================

class ValidacaoCPF(BaseModel):
    cpf: str
    valido: bool
    existe_sistema: bool = False


class ValidacaoMatricula(BaseModel):
    matricula: str
    valido: bool
    existe_sistema: bool = False


class ValidacaoProntuario(BaseModel):
    numero_prontuario: str
    valido: bool
    existe_sistema: bool = False


class ValidacaoCNPJ(BaseModel):
    cnpj: str
    valido: bool
    existe_sistema: bool = False


# ========================= VINCULAR FUNCIONÁRIO A ABRIGO =========================

class VincularFuncionarioAbrigo(BaseModel):
    funcionario_id: int
    abrigo_id: Optional[int] = None


# ========================= TRANSFERÊNCIA =========================

class TransferenciaFuncionario(BaseModel):
    funcionario_id: int
    abrigo_origem_id: Optional[int] = None
    abrigo_destino_id: Optional[int] = None
    motivo: Optional[str] = None
    observacoes: Optional[str] = None


class HistoricoTransferenciaResponse(BaseModel):
    id_transferencia: int
    id_funcionario: int
    id_abrigo_origem: Optional[int] = None
    id_abrigo_destino: Optional[int] = None
    data_transferencia: datetime
    motivo: Optional[str] = None
    observacoes: Optional[str] = None
    
    class Config:
        from_attributes = True


# ========================= RELATÓRIOS =========================

class RelatorioOcupacaoAbrigo(BaseModel):
    abrigo: str
    capacidade_total: int
    ocupacao_atual: int
    vagas_livres: int
    taxa_ocupacao: float
    funcionarios: int
    tipo_abrigo: str
    cidade: str


class RelatorioFuncionariosTurno(BaseModel):
    turno: str
    quantidade: int


class RelatorioAdmissoesPeriodo(BaseModel):
    total_admissoes: int
    admissoes_ativas: int
    admissoes_finalizadas: int
    por_abrigo: dict


# ========================= DASHBOARD =========================

class DashboardData(BaseModel):
    estatisticas: EstatisticasSistema
    abrigos_ocupacao: list
    funcionarios_por_turno: dict
    admissoes_recentes: list


# ========================= RESPONSES ESPECÍFICAS =========================

class LoginResponse(BaseModel):
    """Para futuro sistema de autenticação"""
    token: str
    tipo_token: str
    usuario: str
    perfil: str


class ErroResponse(BaseModel):
    """Response padrão para erros"""
    erro: bool = True
    mensagem: str
    codigo: Optional[int] = None
    detalhes: Optional[dict] = None


class SucessoResponse(BaseModel):
    """Response padrão para sucesso"""
    sucesso: bool = True
    mensagem: str
    dados: Optional[dict] = None