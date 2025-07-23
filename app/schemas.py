from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.models import TipoAbrigo, TurnoEnum, StatusFuncionario, StatusAcolhimento


class AbrigoBase(BaseModel):
    nome: str
    localizacao: str
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


class AbrigoResponse(AbrigoBase):
    id_abrigo: int
    cnpj: str
    ativo: bool
    
    class Config:
        from_attributes = True


class FuncionarioBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    telefone: str
    cargo: str
    turno: TurnoEnum
    matricula: str


class FuncionarioCreate(FuncionarioBase):
    endereco_rua: str
    endereco_bairro: str
    endereco_cidade: str
    endereco_estado: str
    data_admissao: date
    salario: float
    email: Optional[str] = None


class FuncionarioResponse(FuncionarioBase):
    id_funcionario: int
    status_funcionario: StatusFuncionario
    
    class Config:
        from_attributes = True


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
    email: Optional[str] = None


class ProfissionalSaudeResponse(ProfissionalSaudeBase):
    id_funcionario: int
    
    class Config:
        from_attributes = True


class PessoaAcolhidaBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    historico_saude: Optional[str]
    genero: str
    necessidade_especial: bool


class PessoaAcolhidaCreate(PessoaAcolhidaBase):
    telefone_principal: str
    endereco_rua: str
    endereco_bairro: str
    endereco_cidade: str
    endereco_estado: str
    motivo_acolhimento: str
    numero_prontuario: str


class PessoaAcolhidaResponse(PessoaAcolhidaBase):
    id: int
    status_acolhimento: StatusAcolhimento
    
    class Config:
        from_attributes = True


class AdmissaoBase(BaseModel):
    pessoa_id: int
    abrigo_id: int
    data_admissao: date


class AdmissaoCreate(AdmissaoBase):
    numero_vaga: Optional[str] = None


class AdmissaoResponse(AdmissaoBase):
    id_acolhimento: int
    data_saida: Optional[date] = None
    status_ativo: bool
    
    class Config:
        from_attributes = True


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


class FamiliarBase(BaseModel):
    nome: str
    parentesco: str
    telefone_principal: str
    contato_emergencia: bool = False


class FamiliarCreate(FamiliarBase):
    id_acolhido: int


class FamiliarUpdate(BaseModel):
    nome: Optional[str] = None
    parentesco: Optional[str] = None
    telefone_principal: Optional[str] = None
    contato_emergencia: Optional[bool] = None


class FamiliarResponse(FamiliarBase):
    id_familiar: int
    id_acolhido: int
    
    class Config:
        from_attributes = True


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


class AcolhidoBase(BaseModel):
    numero_prontuario: str
    data_entrada: date
    motivo_acolhimento: str


class AcolhidoCreate(AcolhidoBase):
    id_pessoa: int
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
    
    class Config:
        from_attributes = True


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


class AcolhimentoResponse(AcolhimentoBase):
    id_acolhimento: int
    data_saida: Optional[date] = None
    numero_vaga: Optional[str] = None
    status_ativo: bool
    
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
    
    id_pessoa: int
    nome: str
    cpf: str
    telefone_principal: str
    email: Optional[str] = None
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
    
    id_pessoa: int
    nome: str
    cpf: str
    telefone_principal: str
    endereco_completo: str
    
    class Config:
        from_attributes = True


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
    total_admissoes_historico: int


class FiltroFuncionario(BaseModel):
    nome: Optional[str] = None
    cargo: Optional[str] = None
    turno: Optional[TurnoEnum] = None
    status: Optional[StatusFuncionario] = None
    ativo: bool = True


class FiltroAcolhido(BaseModel):
    nome: Optional[str] = None
    numero_prontuario: Optional[str] = None
    status: Optional[StatusAcolhimento] = None
    data_entrada_inicio: Optional[date] = None
    data_entrada_fim: Optional[date] = None


class FiltroAdmissao(BaseModel):
    abrigo_id: Optional[int] = None
    status_ativo: Optional[bool] = None
    data_entrada_inicio: Optional[date] = None
    data_entrada_fim: Optional[date] = None


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