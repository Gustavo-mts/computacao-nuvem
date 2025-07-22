from sqlalchemy.orm import Session
from app import schemas
from datetime import date
from typing import List, Optional
from app.models import (
    Pessoa, Funcionario, Acolhido, Abrigo, Acolhimento, Atendimento, Familiar,
    TipoPessoa, StatusFuncionario, StatusAcolhimento, TurnoEnum, TipoAbrigo
)


def criar_abrigo(db: Session, abrigo: schemas.AbrigoCreate):
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
    return db.query(Abrigo).filter(Abrigo.nome == nome).first()


def buscar_abrigo_por_cnpj(db: Session, cnpj: str):
    return db.query(Abrigo).filter(Abrigo.cnpj == cnpj).first()


def listar_abrigos(db: Session, ativos: bool = True):
    query = db.query(Abrigo)
    if ativos:
        query = query.filter(Abrigo.ativo == True)
    return query.all()


def criar_funcionario(db: Session, funcionario: schemas.FuncionarioCreate):
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
            turno=funcionario.turno
        )
        db.add(db_funcionario)
        db.commit()
        db.refresh(db_funcionario)
        return db_funcionario
        
    except Exception as e:
        db.rollback()
        raise e


def buscar_funcionario_por_matricula(db: Session, matricula: str):
    return db.query(Funcionario).filter(Funcionario.matricula == matricula).first()


def listar_funcionarios(db: Session, ativos: bool = True):
    query = db.query(Funcionario).join(Pessoa)
    if ativos:
        query = query.filter(Funcionario.status_funcionario == StatusFuncionario.ATIVO)
        query = query.filter(Pessoa.ativo == True)
    return query.all()


def criar_profissional_saude(db: Session, profissional: schemas.ProfissionalSaudeCreate):
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


def buscar_pessoa_por_cpf(db: Session, cpf: str):
    return db.query(Pessoa).filter(Pessoa.cpf == cpf).first()


def buscar_pessoa_por_id(db: Session, pessoa_id: int):
    return db.query(Pessoa).filter(Pessoa.id_pessoa == pessoa_id).first()


def listar_pessoas(db: Session, tipo_pessoa: TipoPessoa = None, ativas: bool = True):
    query = db.query(Pessoa)
    if tipo_pessoa:
        query = query.filter(Pessoa.tipo_pessoa == tipo_pessoa)
    if ativas:
        query = query.filter(Pessoa.ativo == True)
    return query.all()


def criar_pessoa_acolhida(db: Session, pessoa_acolhida: schemas.PessoaAcolhidaCreate):
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


def listar_acolhidos(db: Session, ativos: bool = True):
    query = db.query(Acolhido).join(Pessoa)
    if ativos:
        query = query.filter(Acolhido.status_acolhimento == StatusAcolhimento.ATIVO)
        query = query.filter(Pessoa.ativo == True)
    return query.all()


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


def registrar_admissao(db: Session, admissao: schemas.AdmissaoCreate):
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


def listar_admissoes(db: Session, ativas: bool = None):
    query = db.query(Acolhimento)
    if ativas is not None:
        query = query.filter(Acolhimento.status_ativo == ativas)
    return query.all()


def finalizar_admissao(db: Session, admissao_id: int, data_saida: date = None):
    try:
        admissao = db.query(Acolhimento).filter(Acolhimento.id_acolhimento == admissao_id).first()
        if admissao:
            admissao.data_saida = data_saida or date.today()
            admissao.status_ativo = False
            db.commit()
            db.refresh(admissao)
        return admissao
        
    except Exception as e:
        db.rollback()
        raise e


def criar_atendimento(db: Session, atendimento: schemas.AtendimentoCreate):
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


def listar_atendimentos_por_acolhido(db: Session, acolhido_id: int):
    return db.query(Atendimento).filter(Atendimento.id_acolhido == acolhido_id).all()


def listar_atendimentos_por_funcionario(db: Session, funcionario_id: int):
    return db.query(Atendimento).filter(Atendimento.id_funcionario == funcionario_id).all()


def listar_atendimentos(db: Session, limit: int = 100):
    return db.query(Atendimento).limit(limit).all()


def adicionar_familiar(db: Session, familiar: schemas.FamiliarCreate):
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