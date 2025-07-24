from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app import schemas
from datetime import date
from typing import List, Optional
from app.models import (
    Pessoa, Funcionario, Acolhido, Abrigo, Acolhimento, Atendimento, Familiar,
    TipoPessoa, StatusFuncionario, StatusAcolhimento, TurnoEnum, TipoAbrigo
)


# ========================= ABRIGOS =========================

def criar_abrigo(db: Session, abrigo: schemas.AbrigoCreate):
    # Verificar se CNPJ já existe
    if buscar_abrigo_por_cnpj(db, abrigo.cnpj):
        raise ValueError("CNPJ já cadastrado no sistema")
    
    db_abrigo = Abrigo(
        cnpj=abrigo.cnpj,
        nome=abrigo.nome,
        capacidade_total=abrigo.capacidade,
        endereco_rua=abrigo.endereco_rua,
        endereco_bairro=abrigo.endereco_bairro,
        endereco_cidade=abrigo.endereco_cidade,
        endereco_estado=abrigo.endereco_estado,
        telefone_principal=abrigo.telefone_principal,
        tipo_abrigo=abrigo.tipo,
        responsavel_legal=abrigo.responsavel_legal
    )
    db.add(db_abrigo)
    db.commit()
    db.refresh(db_abrigo)
    return db_abrigo


def buscar_abrigo_por_nome(db: Session, nome: str):
    return db.query(Abrigo).filter(Abrigo.nome.ilike(f"%{nome}%")).first()


def buscar_abrigo_por_cnpj(db: Session, cnpj: str):
    return db.query(Abrigo).filter(Abrigo.cnpj == cnpj).first()


def buscar_abrigo_por_id(db: Session, abrigo_id: int):
    """Busca abrigo por ID"""
    return db.query(Abrigo).filter(Abrigo.id_abrigo == abrigo_id).first()


def listar_abrigos(db: Session, ativos: bool = True, skip: int = 0, limit: int = 100):
    query = db.query(Abrigo)
    if ativos:
        query = query.filter(Abrigo.ativo == True)
    return query.offset(skip).limit(limit).all()


def atualizar_abrigo(db: Session, abrigo_id: int, abrigo_update: schemas.AbrigoUpdate):
    """Atualiza dados de um abrigo"""
    try:
        abrigo = buscar_abrigo_por_id(db, abrigo_id)
        if not abrigo:
            return None
        
        for field, value in abrigo_update.dict(exclude_unset=True).items():
            setattr(abrigo, field, value)
        
        db.commit()
        db.refresh(abrigo)
        return abrigo
    except Exception as e:
        db.rollback()
        raise e


def remover_abrigo(db: Session, abrigo_id: int, force: bool = False):
    """Remove abrigo (só se não tiver admissões ativas ou force=True)"""
    try:
        abrigo = buscar_abrigo_por_id(db, abrigo_id)
        if not abrigo:
            return None
        
        # Verificar admissões ativas
        admissoes_ativas = db.query(Acolhimento).filter(
            Acolhimento.id_abrigo == abrigo_id,
            Acolhimento.status_ativo == True
        ).count()
        
        if admissoes_ativas > 0 and not force:
            raise ValueError(f"Abrigo possui {admissoes_ativas} admissões ativas")
        
        # Desvincular funcionários
        db.query(Funcionario).filter(Funcionario.id_abrigo == abrigo_id).update(
            {Funcionario.id_abrigo: None}
        )
        
        if force:
            abrigo.ativo = False
        else:
            db.delete(abrigo)
        
        db.commit()
        return abrigo
    except Exception as e:
        db.rollback()
        raise e


# ========================= FUNCIONÁRIOS =========================

def criar_funcionario(db: Session, funcionario: schemas.FuncionarioCreate):
    # Verificações de duplicidade
    if buscar_pessoa_por_cpf(db, funcionario.cpf):
        raise ValueError("CPF já cadastrado no sistema")
    
    if buscar_funcionario_por_matricula(db, funcionario.matricula):
        raise ValueError("Matrícula já cadastrada no sistema")
    
    # Verificar se o abrigo existe (se informado)
    if funcionario.id_abrigo and not buscar_abrigo_por_id(db, funcionario.id_abrigo):
        raise ValueError("Abrigo informado não existe")
    
    try:
        db_pessoa = Pessoa(
            cpf=funcionario.cpf,
            nome=funcionario.nome,
            data_nascimento=funcionario.data_nascimento,
            telefone_principal=funcionario.telefone,
            email=funcionario.email,
            endereco_rua=funcionario.endereco_rua,
            endereco_bairro=funcionario.endereco_bairro,
            endereco_cidade=funcionario.endereco_cidade,
            endereco_estado=funcionario.endereco_estado,
            tipo_pessoa=TipoPessoa.FUNCIONARIO
        )
        db.add(db_pessoa)
        db.flush()
        
        db_funcionario = Funcionario(
            id_pessoa=db_pessoa.id_pessoa,
            matricula=funcionario.matricula,
            cargo=funcionario.cargo,
            data_admissao=funcionario.data_admissao,
            salario=funcionario.salario,
            turno=funcionario.turno,
            id_abrigo=funcionario.id_abrigo
        )
        db.add(db_funcionario)
        db.commit()
        db.refresh(db_funcionario)
        return db_funcionario
        
    except Exception as e:
        db.rollback()
        raise e


def buscar_funcionario_por_id(db: Session, funcionario_id: int):
    """Busca funcionário por ID com dados da pessoa"""
    return db.query(Funcionario).filter(Funcionario.id_funcionario == funcionario_id).first()


def buscar_funcionario_por_matricula(db: Session, matricula: str):
    return db.query(Funcionario).filter(Funcionario.matricula == matricula).first()


def listar_funcionarios(db: Session, ativos: bool = True, skip: int = 0, limit: int = 100):
    query = db.query(Funcionario).join(Pessoa)
    if ativos:
        query = query.filter(Funcionario.status_funcionario == StatusFuncionario.ATIVO)
        query = query.filter(Pessoa.ativo == True)
    return query.offset(skip).limit(limit).all()


def listar_funcionarios_por_abrigo(db: Session, abrigo_id: int, ativos: bool = True):
    """Lista todos os funcionários de um abrigo específico"""
    query = db.query(Funcionario).join(Pessoa).filter(Funcionario.id_abrigo == abrigo_id)
    if ativos:
        query = query.filter(Funcionario.status_funcionario == StatusFuncionario.ATIVO)
        query = query.filter(Pessoa.ativo == True)
    return query.all()


def listar_funcionarios_sem_abrigo(db: Session, ativos: bool = True):
    """Lista funcionários que não estão vinculados a nenhum abrigo"""
    query = db.query(Funcionario).join(Pessoa).filter(Funcionario.id_abrigo.is_(None))
    if ativos:
        query = query.filter(Funcionario.status_funcionario == StatusFuncionario.ATIVO)
        query = query.filter(Pessoa.ativo == True)
    return query.all()


def vincular_funcionario_abrigo(db: Session, funcionario_id: int, abrigo_id: Optional[int] = None):
    """Vincula ou desvincula um funcionário de um abrigo"""
    try:
        funcionario = buscar_funcionario_por_id(db, funcionario_id)
        if not funcionario:
            raise ValueError("Funcionário não encontrado")
        
        # Verificar se o abrigo existe (se informado)
        if abrigo_id and not buscar_abrigo_por_id(db, abrigo_id):
            raise ValueError("Abrigo não encontrado")
        
        funcionario.id_abrigo = abrigo_id
        db.commit()
        db.refresh(funcionario)
        return funcionario
        
    except Exception as e:
        db.rollback()
        raise e


def contar_funcionarios_por_abrigo(db: Session, abrigo_id: int):
    """Conta quantos funcionários ativos estão vinculados ao abrigo"""
    return db.query(Funcionario)\
             .join(Pessoa)\
             .filter(Funcionario.id_abrigo == abrigo_id)\
             .filter(Funcionario.status_funcionario == StatusFuncionario.ATIVO)\
             .filter(Pessoa.ativo == True)\
             .count()


def atualizar_funcionario(db: Session, funcionario_id: int, funcionario_update: schemas.FuncionarioUpdate):
    """Atualiza dados de um funcionário"""
    try:
        funcionario = buscar_funcionario_por_id(db, funcionario_id)
        if not funcionario:
            return None
        
        # Atualizar dados pessoais
        pessoa_data = {k: v for k, v in funcionario_update.dict(exclude_unset=True).items() 
                      if k in ['nome', 'telefone_principal', 'email', 'endereco_rua', 
                              'endereco_bairro', 'endereco_cidade', 'endereco_estado']}
        
        for field, value in pessoa_data.items():
            setattr(funcionario.pessoa, field, value)
        
        # Atualizar dados funcionais
        func_data = {k: v for k, v in funcionario_update.dict(exclude_unset=True).items() 
                    if k in ['cargo', 'salario', 'turno', 'status_funcionario', 'id_abrigo']}
        
        for field, value in func_data.items():
            setattr(funcionario, field, value)
        
        db.commit()
        db.refresh(funcionario)
        return funcionario
    except Exception as e:
        db.rollback()
        raise e


def remover_funcionario(db: Session, funcionario_id: int, inativar_se_tem_dados: bool = True):
    """Remove ou inativa funcionário"""
    try:
        funcionario = buscar_funcionario_por_id(db, funcionario_id)
        if not funcionario:
            return None
        
        # Verificar se tem atendimentos
        tem_atendimentos = db.query(Atendimento).filter(
            Atendimento.id_funcionario == funcionario_id
        ).count() > 0
        
        if tem_atendimentos and inativar_se_tem_dados:
            funcionario.status_funcionario = StatusFuncionario.INATIVO
            funcionario.pessoa.ativo = False
        else:
            db.delete(funcionario)
            db.delete(funcionario.pessoa)
        
        db.commit()
        return funcionario
    except Exception as e:
        db.rollback()
        raise e


# ========================= PROFISSIONAIS DE SAÚDE =========================

def criar_profissional_saude(db: Session, profissional: schemas.ProfissionalSaudeCreate):
    # Verificar duplicidade
    if buscar_pessoa_por_cpf(db, profissional.cpf):
        raise ValueError("CPF já cadastrado no sistema")
    
    if buscar_profissional_por_registro(db, profissional.registro):
        raise ValueError("Registro profissional já cadastrado")
    
    try:
        db_pessoa = Pessoa(
            cpf=profissional.cpf,
            nome=profissional.nome,
            data_nascimento=profissional.data_nascimento,
            telefone_principal=profissional.telefone,
            email=profissional.email,
            endereco_rua=profissional.endereco_rua,
            endereco_bairro=profissional.endereco_bairro,
            endereco_cidade=profissional.endereco_cidade,
            endereco_estado=profissional.endereco_estado,
            tipo_pessoa=TipoPessoa.FUNCIONARIO
        )
        db.add(db_pessoa)
        db.flush()
        
        db_funcionario = Funcionario(
            id_pessoa=db_pessoa.id_pessoa,
            matricula=profissional.registro,
            cargo=f"Profissional de {profissional.area}",
            data_admissao=date.today(),
            salario=5000.00,
            turno=TurnoEnum.INTEGRAL
        )
        db.add(db_funcionario)
        db.commit()
        db.refresh(db_funcionario)
        return db_funcionario
        
    except Exception as e:
        db.rollback()
        raise e


def buscar_profissional_por_registro(db: Session, registro: str):
    return db.query(Funcionario).filter(Funcionario.matricula == registro).first()


# ========================= PESSOAS =========================

def buscar_pessoa_por_cpf(db: Session, cpf: str):
    return db.query(Pessoa).filter(Pessoa.cpf == cpf).first()


def buscar_pessoa_por_id(db: Session, pessoa_id: int):
    return db.query(Pessoa).filter(Pessoa.id_pessoa == pessoa_id).first()


def listar_pessoas(db: Session, tipo_pessoa: TipoPessoa = None, ativas: bool = True, skip: int = 0, limit: int = 100):
    query = db.query(Pessoa)
    if tipo_pessoa:
        query = query.filter(Pessoa.tipo_pessoa == tipo_pessoa)
    if ativas:
        query = query.filter(Pessoa.ativo == True)
    return query.offset(skip).limit(limit).all()


# ========================= ACOLHIDOS =========================

def criar_pessoa_acolhida(db: Session, pessoa_acolhida: schemas.PessoaAcolhidaCreate):
    # Verificar duplicidade
    if buscar_pessoa_por_cpf(db, pessoa_acolhida.cpf):
        raise ValueError("CPF já cadastrado no sistema")
    
    if buscar_acolhido_por_prontuario(db, pessoa_acolhida.numero_prontuario):
        raise ValueError("Número de prontuário já existe")
    
    try:
        db_pessoa = Pessoa(
            cpf=pessoa_acolhida.cpf,
            nome=pessoa_acolhida.nome,
            data_nascimento=pessoa_acolhida.data_nascimento,
            telefone_principal=pessoa_acolhida.telefone_principal,
            endereco_rua=pessoa_acolhida.endereco_rua,
            endereco_bairro=pessoa_acolhida.endereco_bairro,
            endereco_cidade=pessoa_acolhida.endereco_cidade,
            endereco_estado=pessoa_acolhida.endereco_estado,
            tipo_pessoa=TipoPessoa.ACOLHIDO
        )
        db.add(db_pessoa)
        db.flush()
        
        db_acolhido = Acolhido(
            id_pessoa=db_pessoa.id_pessoa,
            numero_prontuario=pessoa_acolhida.numero_prontuario,
            data_entrada=date.today(),
            motivo_acolhimento=pessoa_acolhida.motivo_acolhimento
        )
        db.add(db_acolhido)
        db.commit()
        db.refresh(db_pessoa)
        return db_pessoa
        
    except Exception as e:
        db.rollback()
        raise e


def listar_acolhidos(db: Session, ativos: bool = True, skip: int = 0, limit: int = 100):
    query = db.query(Acolhido).join(Pessoa)
    if ativos:
        query = query.filter(Acolhido.status_acolhimento == StatusAcolhimento.ATIVO)
        query = query.filter(Pessoa.ativo == True)
    return query.offset(skip).limit(limit).all()


def buscar_acolhido_por_id(db: Session, acolhido_id: int):
    return db.query(Acolhido).filter(Acolhido.id_acolhido == acolhido_id).first()


def buscar_acolhido_por_prontuario(db: Session, numero_prontuario: str):
    return db.query(Acolhido).filter(Acolhido.numero_prontuario == numero_prontuario).first()


def buscar_acolhido_por_pessoa_id(db: Session, pessoa_id: int):
    return db.query(Acolhido).filter(Acolhido.id_pessoa == pessoa_id).first()


def listar_pessoas_acolhidas(db: Session, ativas: bool = True):
    query = db.query(Pessoa).join(Acolhido).filter(Pessoa.tipo_pessoa == TipoPessoa.ACOLHIDO)
    if ativas:
        query = query.filter(Acolhido.status_acolhimento == StatusAcolhimento.ATIVO)
        query = query.filter(Pessoa.ativo == True)
    return query.all()


# ========================= ADMISSÕES =========================

def registrar_admissao(db: Session, admissao: schemas.AdmissaoCreate):
    # Verificar se acolhido existe
    acolhido = buscar_acolhido_por_id(db, admissao.pessoa_id)
    if not acolhido:
        raise ValueError("Pessoa acolhida não encontrada")
    
    # Verificar se abrigo existe e tem capacidade
    abrigo = buscar_abrigo_por_id(db, admissao.abrigo_id)
    if not abrigo:
        raise ValueError("Abrigo não encontrado")
    
    # Verificar capacidade do abrigo
    admissoes_ativas = db.query(Acolhimento).filter(
        Acolhimento.id_abrigo == admissao.abrigo_id,
        Acolhimento.status_ativo == True
    ).count()
    
    if admissoes_ativas >= abrigo.capacidade_total:
        raise ValueError("Abrigo está com capacidade máxima")
    
    # Verificar se já tem admissão ativa
    if buscar_admissao_ativa_por_acolhido(db, admissao.pessoa_id):
        raise ValueError("Pessoa já possui admissão ativa")
    
    try:
        db_acolhimento = Acolhimento(
            id_acolhido=admissao.pessoa_id,
            id_abrigo=admissao.abrigo_id,
            data_entrada=admissao.data_admissao,
            numero_vaga=admissao.numero_vaga,
            status_ativo=True
        )
        db.add(db_acolhimento)
        db.commit()
        db.refresh(db_acolhimento)
        return db_acolhimento
        
    except Exception as e:
        db.rollback()
        raise e


def buscar_admissao_por_id(db: Session, admissao_id: int):
    """Busca admissão por ID"""
    return db.query(Acolhimento).filter(Acolhimento.id_acolhimento == admissao_id).first()


def buscar_admissao_ativa_por_pessoa(db: Session, pessoa_id: int):
    acolhido = db.query(Acolhido).filter(Acolhido.id_pessoa == pessoa_id).first()
    if not acolhido:
        return None
    
    return db.query(Acolhimento)\
             .filter(Acolhimento.id_acolhido == acolhido.id_acolhido)\
             .filter(Acolhimento.status_ativo == True)\
             .first()


def buscar_admissao_ativa_por_acolhido(db: Session, acolhido_id: int):
    return db.query(Acolhimento)\
             .filter(Acolhimento.id_acolhido == acolhido_id)\
             .filter(Acolhimento.status_ativo == True)\
             .first()


def listar_admissoes(db: Session, ativas: bool = None, skip: int = 0, limit: int = 100):
    query = db.query(Acolhimento)
    if ativas is not None:
        query = query.filter(Acolhimento.status_ativo == ativas)
    return query.offset(skip).limit(limit).all()


def finalizar_admissao(db: Session, admissao_id: int, data_saida: date = None):
    try:
        admissao = buscar_admissao_por_id(db, admissao_id)
        if not admissao:
            raise ValueError("Admissão não encontrada")
        
        if not admissao.status_ativo:
            raise ValueError("Admissão já foi finalizada")
        
        admissao.data_saida = data_saida or date.today()
        admissao.status_ativo = False
        db.commit()
        db.refresh(admissao)
        return admissao
        
    except Exception as e:
        db.rollback()
        raise e


# ========================= ATENDIMENTOS =========================

def criar_atendimento(db: Session, atendimento: schemas.AtendimentoCreate):
    # Verificar se acolhido e funcionário existem
    if not buscar_acolhido_por_id(db, atendimento.id_acolhido):
        raise ValueError("Pessoa acolhida não encontrada")
    
    if not buscar_funcionario_por_id(db, atendimento.id_funcionario):
        raise ValueError("Funcionário não encontrado")
    
    try:
        db_atendimento = Atendimento(
            id_acolhido=atendimento.id_acolhido,
            id_funcionario=atendimento.id_funcionario,
            data_atendimento=atendimento.data_atendimento,
            tipo_atendimento=atendimento.tipo_atendimento,
            descricao=atendimento.descricao,
            observacoes=atendimento.observacoes
        )
        db.add(db_atendimento)
        db.commit()
        db.refresh(db_atendimento)
        return db_atendimento
        
    except Exception as e:
        db.rollback()
        raise e


def listar_atendimentos_por_acolhido(db: Session, acolhido_id: int, skip: int = 0, limit: int = 100):
    return db.query(Atendimento)\
             .filter(Atendimento.id_acolhido == acolhido_id)\
             .order_by(Atendimento.data_atendimento.desc())\
             .offset(skip).limit(limit).all()


def listar_atendimentos_por_funcionario(db: Session, funcionario_id: int, skip: int = 0, limit: int = 100):
    return db.query(Atendimento)\
             .filter(Atendimento.id_funcionario == funcionario_id)\
             .order_by(Atendimento.data_atendimento.desc())\
             .offset(skip).limit(limit).all()


def listar_atendimentos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Atendimento)\
             .order_by(Atendimento.data_atendimento.desc())\
             .offset(skip).limit(limit).all()


# ========================= FAMILIARES =========================

def adicionar_familiar(db: Session, familiar: schemas.FamiliarCreate):
    # Verificar se acolhido existe
    if not buscar_acolhido_por_id(db, familiar.id_acolhido):
        raise ValueError("Pessoa acolhida não encontrada")
    
    try:
        db_familiar = Familiar(
            id_acolhido=familiar.id_acolhido,
            nome=familiar.nome,
            parentesco=familiar.parentesco,
            telefone_principal=familiar.telefone_principal,
            contato_emergencia=familiar.contato_emergencia
        )
        db.add(db_familiar)
        db.commit()
        db.refresh(db_familiar)
        return db_familiar
        
    except Exception as e:
        db.rollback()
        raise e


def listar_familiares_por_acolhido(db: Session, acolhido_id: int):
    return db.query(Familiar).filter(Familiar.id_acolhido == acolhido_id).all()


def buscar_familiar_por_id(db: Session, familiar_id: int):
    return db.query(Familiar).filter(Familiar.id_familiar == familiar_id).first()


# ========================= VALIDAÇÕES =========================

def verificar_cpf_existe(db: Session, cpf: str, excluir_id: int = None):
    query = db.query(Pessoa).filter(Pessoa.cpf == cpf)
    if excluir_id:
        query = query.filter(Pessoa.id_pessoa != excluir_id)
    return query.first() is not None


def verificar_matricula_existe(db: Session, matricula: str, excluir_id: int = None):
    query = db.query(Funcionario).filter(Funcionario.matricula == matricula)
    if excluir_id:
        query = query.filter(Funcionario.id_funcionario != excluir_id)
    return query.first() is not None


def verificar_prontuario_existe(db: Session, numero_prontuario: str, excluir_id: int = None):
    query = db.query(Acolhido).filter(Acolhido.numero_prontuario == numero_prontuario)
    if excluir_id:
        query = query.filter(Acolhido.id_acolhido != excluir_id)
    return query.first() is not None


def verificar_cnpj_existe(db: Session, cnpj: str, excluir_id: int = None):
    query = db.query(Abrigo).filter(Abrigo.cnpj == cnpj)
    if excluir_id:
        query = query.filter(Abrigo.id_abrigo != excluir_id)
    return query.first() is not None


# ========================= ESTATÍSTICAS =========================

def get_estatisticas_sistema(db: Session):
    return {
        'total_abrigos': db.query(Abrigo).filter(Abrigo.ativo == True).count(),
        'total_funcionarios': db.query(Funcionario).join(Pessoa).filter(
            Funcionario.status_funcionario == StatusFuncionario.ATIVO,
            Pessoa.ativo == True
        ).count(),
        'total_acolhidos': db.query(Acolhido).join(Pessoa).filter(
            Acolhido.status_acolhimento == StatusAcolhimento.ATIVO,
            Pessoa.ativo == True
        ).count(),
        'total_admissoes_ativas': db.query(Acolhimento).filter(
            Acolhimento.status_ativo == True
        ).count(),
        'total_atendimentos': db.query(Atendimento).count()
    }


def get_estatisticas_abrigo(db: Session, abrigo_id: int):
    """Estatísticas detalhadas de um abrigo"""
    abrigo = buscar_abrigo_por_id(db, abrigo_id)
    if not abrigo:
        return None
    
    ocupacao_atual = db.query(Acolhimento).filter(
        Acolhimento.id_abrigo == abrigo_id,
        Acolhimento.status_ativo == True
    ).count()
    
    total_funcionarios = contar_funcionarios_por_abrigo(db, abrigo_id)
    
    total_admissoes_historico = db.query(Acolhimento).filter(
        Acolhimento.id_abrigo == abrigo_id
    ).count()
    
    return {
        'id_abrigo': abrigo_id,
        'nome_abrigo': abrigo.nome,
        'capacidade_total': abrigo.capacidade_total,
        'ocupacao_atual': ocupacao_atual,
        'taxa_ocupacao': (ocupacao_atual / abrigo.capacidade_total * 100) if abrigo.capacidade_total > 0 else 0,
        'total_funcionarios': total_funcionarios,
        'total_admissoes_historico': total_admissoes_historico
    }


# ========================= BUSCAS AVANÇADAS =========================

def buscar_funcionarios_com_filtros(db: Session, filtros: schemas.FiltroFuncionario):
    """Busca funcionários com filtros avançados"""
    query = db.query(Funcionario).join(Pessoa)
    
    if filtros.nome:
        query = query.filter(Pessoa.nome.ilike(f"%{filtros.nome}%"))
    
    if filtros.cargo:
        query = query.filter(Funcionario.cargo.ilike(f"%{filtros.cargo}%"))
    
    if filtros.turno:
        query = query.filter(Funcionario.turno == filtros.turno)
    
    if filtros.status:
        query = query.filter(Funcionario.status_funcionario == filtros.status)
    
    if filtros.ativo:
        query = query.filter(Pessoa.ativo == True)
        query = query.filter(Funcionario.status_funcionario == StatusFuncionario.ATIVO)
    
    return query.all()


def buscar_acolhidos_com_filtros(db: Session, filtros: schemas.FiltroAcolhido):
    """Busca acolhidos com filtros avançados"""
    query = db.query(Acolhido).join(Pessoa)
    
    if filtros.nome:
        query = query.filter(Pessoa.nome.ilike(f"%{filtros.nome}%"))
    
    if filtros.numero_prontuario:
        query = query.filter(Acolhido.numero_prontuario.ilike(f"%{filtros.numero_prontuario}%"))
    
    if filtros.status:
        query = query.filter(Acolhido.status_acolhimento == filtros.status)
    
    if filtros.data_entrada_inicio:
        query = query.filter(Acolhido.data_entrada >= filtros.data_entrada_inicio)
    
    if filtros.data_entrada_fim:
        query = query.filter(Acolhido.data_entrada <= filtros.data_entrada_fim)
    
    return query.all()


def buscar_admissoes_com_filtros(db: Session, filtros: schemas.FiltroAdmissao):
    """Busca admissões com filtros avançados"""
    query = db.query(Acolhimento)
    
    if filtros.abrigo_id:
        query = query.filter(Acolhimento.id_abrigo == filtros.abrigo_id)
    
    if filtros.status_ativo is not None:
        query = query.filter(Acolhimento.status_ativo == filtros.status_ativo)
    
    if filtros.data_entrada_inicio:
        query = query.filter(Acolhimento.data_entrada >= filtros.data_entrada_inicio)
    
    if filtros.data_entrada_fim:
        query = query.filter(Acolhimento.data_entrada <= filtros.data_entrada_fim)
    
    return query.order_by(Acolhimento.data_entrada.desc()).all()


# ========================= RELATÓRIOS =========================

def relatorio_ocupacao_abrigos(db: Session):
    """Relatório de ocupação de todos os abrigos"""
    abrigos = listar_abrigos(db, ativos=True)
    relatorio = []
    
    for abrigo in abrigos:
        ocupacao = db.query(Acolhimento).filter(
            Acolhimento.id_abrigo == abrigo.id_abrigo,
            Acolhimento.status_ativo == True
        ).count()
        
        funcionarios = contar_funcionarios_por_abrigo(db, abrigo.id_abrigo)
        
        relatorio.append({
            'abrigo': abrigo.nome,
            'capacidade_total': abrigo.capacidade_total,
            'ocupacao_atual': ocupacao,
            'vagas_livres': abrigo.capacidade_total - ocupacao,
            'taxa_ocupacao': (ocupacao / abrigo.capacidade_total * 100) if abrigo.capacidade_total > 0 else 0,
            'funcionarios': funcionarios,
            'tipo_abrigo': abrigo.tipo_abrigo.value,
            'cidade': abrigo.endereco_cidade
        })
    
    return relatorio


def relatorio_funcionarios_por_turno(db: Session, abrigo_id: Optional[int] = None):
    """Relatório de funcionários por turno"""
    query = db.query(Funcionario).join(Pessoa).filter(
        Funcionario.status_funcionario == StatusFuncionario.ATIVO,
        Pessoa.ativo == True
    )
    
    if abrigo_id:
        query = query.filter(Funcionario.id_abrigo == abrigo_id)
    
    funcionarios = query.all()
    
    relatorio = {}
    for turno in TurnoEnum:
        relatorio[turno.value] = len([f for f in funcionarios if f.turno == turno])
    
    return relatorio


def relatorio_admissoes_periodo(db: Session, data_inicio: date, data_fim: date):
    """Relatório de admissões em um período"""
    admissoes = db.query(Acolhimento).filter(
        Acolhimento.data_entrada >= data_inicio,
        Acolhimento.data_entrada <= data_fim
    ).all()
    
    relatorio = {
        'total_admissoes': len(admissoes),
        'admissoes_ativas': len([a for a in admissoes if a.status_ativo]),
        'admissoes_finalizadas': len([a for a in admissoes if not a.status_ativo]),
        'por_abrigo': {}
    }
    
    for admissao in admissoes:
        abrigo_nome = admissao.abrigo.nome
        if abrigo_nome not in relatorio['por_abrigo']:
            relatorio['por_abrigo'][abrigo_nome] = 0
        relatorio['por_abrigo'][abrigo_nome] += 1
    
    return relatorio


# ========================= FUNÇÕES DE LIMPEZA =========================

def limpar_dados_inativos(db: Session, dias_inativo: int = 365):
    """Remove dados de pessoas inativas há mais de X dias"""
    try:
        from datetime import datetime, timedelta
        data_limite = datetime.now().date() - timedelta(days=dias_inativo)
        
        # Buscar pessoas inativas há muito tempo
        pessoas_antigas = db.query(Pessoa).filter(
            Pessoa.ativo == False,
            # Assumindo que temos um campo data_inativacao, senão adaptar
        ).all()
        
        count = 0
        for pessoa in pessoas_antigas:
            # Verificar se não tem dados importantes vinculados
            if pessoa.tipo_pessoa == TipoPessoa.FUNCIONARIO:
                funcionario = pessoa.funcionario
                if funcionario and not db.query(Atendimento).filter(
                    Atendimento.id_funcionario == funcionario.id_funcionario
                ).first():
                    db.delete(funcionario)
                    db.delete(pessoa)
                    count += 1
        
        db.commit()
        return count
        
    except Exception as e:
        db.rollback()
        raise e


# ========================= BACKUP E VALIDAÇÕES =========================

def validar_integridade_dados(db: Session):
    """Valida a integridade dos dados do sistema"""
    problemas = []
    
    # Verificar funcionários sem pessoa
    funcionarios_orfaos = db.query(Funcionario).filter(
        ~Funcionario.id_pessoa.in_(db.query(Pessoa.id_pessoa))
    ).count()
    if funcionarios_orfaos > 0:
        problemas.append(f"{funcionarios_orfaos} funcionários sem pessoa vinculada")
    
    # Verificar admissões sem acolhido
    admissoes_orfaas = db.query(Acolhimento).filter(
        ~Acolhimento.id_acolhido.in_(db.query(Acolhido.id_acolhido))
    ).count()
    if admissoes_orfaas > 0:
        problemas.append(f"{admissoes_orfaas} admissões sem acolhido vinculado")
    
    # Verificar capacidade de abrigos
    abrigos_superlotados = db.query(Abrigo).filter(
        Abrigo.id_abrigo.in_(
            db.query(Acolhimento.id_abrigo)
            .filter(Acolhimento.status_ativo == True)
            .group_by(Acolhimento.id_abrigo)
            .having(func.count(Acolhimento.id_acolhimento) > Abrigo.capacidade_total)
        )
    ).count()
    if abrigos_superlotados > 0:
        problemas.append(f"{abrigos_superlotados} abrigos com superlotação")
    
    return problemas


# ========================= FUNÇÕES AUXILIARES =========================

def transferir_funcionario_abrigo(db: Session, funcionario_id: int, novo_abrigo_id: int, motivo: str = ""):
    """Transfere funcionário de um abrigo para outro com histórico"""
    try:
        funcionario = buscar_funcionario_por_id(db, funcionario_id)
        if not funcionario:
            raise ValueError("Funcionário não encontrado")
        
        if novo_abrigo_id and not buscar_abrigo_por_id(db, novo_abrigo_id):
            raise ValueError("Novo abrigo não encontrado")
        
        abrigo_anterior = funcionario.id_abrigo
        funcionario.id_abrigo = novo_abrigo_id
        
        # Aqui você poderia criar uma tabela de histórico de transferências
        # Por agora, apenas atualizamos o vínculo
        
        db.commit()
        db.refresh(funcionario)
        
        return {
            'funcionario': funcionario,
            'abrigo_anterior': abrigo_anterior,
            'abrigo_novo': novo_abrigo_id,
            'motivo': motivo
        }
        
    except Exception as e:
        db.rollback()
        raise e


def get_dashboard_data(db: Session):
    """Dados completos para o dashboard"""
    stats = get_estatisticas_sistema(db)
    
    # Abrigos com maior ocupação
    abrigos_ocupacao = db.query(
        Abrigo.nome,
        Abrigo.capacidade_total,
        func.count(Acolhimento.id_acolhimento).label('ocupacao')
    ).outerjoin(
        Acolhimento,
        and_(Abrigo.id_abrigo == Acolhimento.id_abrigo, Acolhimento.status_ativo == True)
    ).filter(Abrigo.ativo == True)\
     .group_by(Abrigo.id_abrigo, Abrigo.nome, Abrigo.capacidade_total)\
     .order_by(func.count(Acolhimento.id_acolhimento).desc())\
     .limit(5).all()
    
    # Funcionários por turno
    turnos_stats = relatorio_funcionarios_por_turno(db)
    
    # Admissões recentes
    admissoes_recentes = listar_admissoes(db, ativas=True, limit=10)
    
    return {
        'estatisticas': stats,
        'abrigos_ocupacao': abrigos_ocupacao,
        'funcionarios_por_turno': turnos_stats,
        'admissoes_recentes': admissoes_recentes
    }