#!/usr/bin/env python3
"""
Script para popular o banco de dados - Sistema de Abrigos
Remove todos os dados existentes e insere 10 tuplas por tabela
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import (
    Base, Pessoa, Funcionario, Acolhido, Abrigo, Acolhimento, 
    Atendimento, Familiar, TipoPessoa, StatusFuncionario, 
    StatusAcolhimento, TurnoEnum, TipoAbrigo
)
from datetime import date
from decimal import Decimal


def seed_database():
    """Remove e popula o banco com dados de teste"""
    
    print("Removendo tabelas existentes...")
    Base.metadata.drop_all(bind=engine)
    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("Inserindo dados de teste...")
        
        # 1. ABRIGOS
        print("Inserindo abrigos...")
        abrigos = [
            Abrigo(cnpj='12.345.678/0001-90', nome='Casa de Acolhimento São Francisco', capacidade_total=30, endereco_rua='Rua São Francisco', endereco_numero='100', endereco_bairro='Centro', endereco_cidade='Fortaleza', endereco_estado='CE', endereco_cep='60000-001', telefone_principal='(85) 3234-1000', tipo_abrigo=TipoAbrigo.MASCULINO, responsavel_legal='Padre João Silva'),
            Abrigo(cnpj='23.456.789/0001-01', nome='Lar Feminino Santa Clara', capacidade_total=25, endereco_rua='Av. da Universidade', endereco_numero='200', endereco_bairro='Benfica', endereco_cidade='Fortaleza', endereco_estado='CE', endereco_cep='60020-001', telefone_principal='(85) 3234-2000', tipo_abrigo=TipoAbrigo.FEMININO, responsavel_legal='Irmã Maria José'),
            Abrigo(cnpj='34.567.890/0001-12', nome='Abrigo Familiar Esperança', capacidade_total=40, endereco_rua='Rua da Harmonia', endereco_numero='300', endereco_bairro='Aldeota', endereco_cidade='Fortaleza', endereco_estado='CE', endereco_cep='60150-001', telefone_principal='(85) 3234-3000', tipo_abrigo=TipoAbrigo.FAMILIAR, responsavel_legal='Dr. Carlos Mendes'),
            Abrigo(cnpj='45.678.901/0001-23', nome='Casa Mista Vida Nova', capacidade_total=35, endereco_rua='Av. Washington Soares', endereco_numero='400', endereco_bairro='Edson Queiroz', endereco_cidade='Fortaleza', endereco_estado='CE', endereco_cep='60811-001', telefone_principal='(85) 3234-4000', tipo_abrigo=TipoAbrigo.MISTO, responsavel_legal='Dra. Ana Beatriz'),
            Abrigo(cnpj='56.789.012/0001-34', nome='Abrigo Masculino Recomeço', capacidade_total=28, endereco_rua='Rua Coronel Correia', endereco_numero='500', endereco_bairro='José Bonifácio', endereco_cidade='Fortaleza', endereco_estado='CE', endereco_cep='60055-001', telefone_principal='(85) 3234-5000', tipo_abrigo=TipoAbrigo.MASCULINO, responsavel_legal='Pastor Marcos Lima'),
            Abrigo(cnpj='67.890.123/0001-45', nome='Casa Feminina Amor e Paz', capacidade_total=32, endereco_rua='Rua Santa Teresinha', endereco_numero='600', endereco_bairro='Messejana', endereco_cidade='Fortaleza', endereco_estado='CE', endereco_cep='60840-001', telefone_principal='(85) 3234-6000', tipo_abrigo=TipoAbrigo.FEMININO, responsavel_legal='Dra. Tereza Santos'),
            Abrigo(cnpj='78.901.234/0001-56', nome='Abrigo Misto Solidariedade', capacidade_total=45, endereco_rua='Av. Alberto Magno', endereco_numero='700', endereco_bairro='Maraponga', endereco_cidade='Fortaleza', endereco_estado='CE', endereco_cep='60710-001', telefone_principal='(85) 3234-7000', tipo_abrigo=TipoAbrigo.MISTO, responsavel_legal='Sr. Roberto Alves'),
            Abrigo(cnpj='89.012.345/0001-67', nome='Casa Familiar Novo Horizonte', capacidade_total=38, endereco_rua='Rua João Cordeiro', endereco_numero='800', endereco_bairro='Cocó', endereco_cidade='Fortaleza', endereco_estado='CE', endereco_cep='60192-001', telefone_principal='(85) 3234-8000', tipo_abrigo=TipoAbrigo.FAMILIAR, responsavel_legal='Sra. Lúcia Fernandes'),
            Abrigo(cnpj='90.123.456/0001-78', nome='Abrigo Masculino São José', capacidade_total=42, endereco_rua='Rua Major Facundo', endereco_numero='900', endereco_bairro='Centro', endereco_cidade='Fortaleza', endereco_estado='CE', endereco_cep='60025-001', telefone_principal='(85) 3234-9000', tipo_abrigo=TipoAbrigo.MASCULINO, responsavel_legal='Frei Antonio Carlos'),
            Abrigo(cnpj='01.234.567/0001-89', nome='Lar Misto Fraternidade', capacidade_total=50, endereco_rua='Av. Desembargador Moreira', endereco_numero='1000', endereco_bairro='Aldeota', endereco_cidade='Fortaleza', endereco_estado='CE', endereco_cep='60170-001', telefone_principal='(85) 3234-0100', tipo_abrigo=TipoAbrigo.MISTO, responsavel_legal='Dr. Fernando Costa')
        ]
        
        for abrigo in abrigos:
            db.add(abrigo)
        db.flush()
        print(f"   {len(abrigos)} abrigos inseridos")
        
        # 2. FUNCIONÁRIOS
        print("Inserindo funcionários...")
        pessoas_funcionarios = [
            {'cpf': '123.456.789-01', 'nome': 'Maria Silva Santos', 'data_nascimento': date(1985, 3, 15), 'telefone_principal': '(85) 98765-4321', 'telefone_secundario': '(85) 3234-5678', 'email': 'maria.silva@email.com', 'endereco_rua': 'Rua das Flores', 'endereco_numero': '123', 'endereco_bairro': 'Centro', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60000-000', 'matricula': 'FUNC001', 'cargo': 'Assistente Social', 'data_admissao': date(2023, 1, 15), 'salario': Decimal('3500.00'), 'turno': TurnoEnum.MANHA},
            {'cpf': '234.567.890-12', 'nome': 'João Carlos Oliveira', 'data_nascimento': date(1990, 7, 22), 'telefone_principal': '(85) 99876-5432', 'telefone_secundario': None, 'email': 'joao.carlos@email.com', 'endereco_rua': 'Av. Beira Mar', 'endereco_numero': '456', 'endereco_bairro': 'Mucuripe', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60165-000', 'matricula': 'FUNC002', 'cargo': 'Psicólogo', 'data_admissao': date(2023, 2, 20), 'salario': Decimal('4000.00'), 'turno': TurnoEnum.TARDE},
            {'cpf': '345.678.901-23', 'nome': 'Ana Paula Costa', 'data_nascimento': date(1988, 11, 30), 'telefone_principal': '(85) 97654-3210', 'telefone_secundario': '(85) 3345-6789', 'email': 'ana.paula@email.com', 'endereco_rua': 'Rua do Sol', 'endereco_numero': '789', 'endereco_bairro': 'Aldeota', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60150-000', 'matricula': 'FUNC003', 'cargo': 'Coordenadora', 'data_admissao': date(2022, 6, 10), 'salario': Decimal('5500.00'), 'turno': TurnoEnum.INTEGRAL},
            {'cpf': '456.789.012-34', 'nome': 'Carlos Roberto Lima', 'data_nascimento': date(1975, 5, 10), 'telefone_principal': '(85) 96543-2109', 'telefone_secundario': None, 'email': 'carlos.lima@email.com', 'endereco_rua': 'Rua da Paz', 'endereco_numero': '321', 'endereco_bairro': 'Benfica', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60020-000', 'matricula': 'FUNC004', 'cargo': 'Educador Social', 'data_admissao': date(2023, 3, 5), 'salario': Decimal('2800.00'), 'turno': TurnoEnum.NOITE},
            {'cpf': '567.890.123-45', 'nome': 'Luciana Ferreira', 'data_nascimento': date(1992, 9, 18), 'telefone_principal': '(85) 95432-1098', 'telefone_secundario': '(85) 3456-7890', 'email': 'luciana.ferreira@email.com', 'endereco_rua': 'Av. Santos Dumont', 'endereco_numero': '654', 'endereco_bairro': 'Papicu', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60175-000', 'matricula': 'FUNC005', 'cargo': 'Enfermeira', 'data_admissao': date(2023, 4, 12), 'salario': Decimal('4200.00'), 'turno': TurnoEnum.MANHA},
            {'cpf': '678.901.234-56', 'nome': 'Ricardo Mendes Silva', 'data_nascimento': date(1987, 12, 8), 'telefone_principal': '(85) 94321-0987', 'telefone_secundario': None, 'email': 'ricardo.mendes@email.com', 'endereco_rua': 'Rua Barão de Studart', 'endereco_numero': '987', 'endereco_bairro': 'Meireles', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60160-000', 'matricula': 'FUNC006', 'cargo': 'Administrador', 'data_admissao': date(2023, 5, 18), 'salario': Decimal('4500.00'), 'turno': TurnoEnum.TARDE},
            {'cpf': '789.012.345-67', 'nome': 'Patricia Rocha Alves', 'data_nascimento': date(1991, 2, 14), 'telefone_principal': '(85) 93210-9876', 'telefone_secundario': '(85) 3567-8901', 'email': 'patricia.rocha@email.com', 'endereco_rua': 'Av. Pontes Vieira', 'endereco_numero': '1234', 'endereco_bairro': 'São Gerardo', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60325-000', 'matricula': 'FUNC007', 'cargo': 'Nutricionista', 'data_admissao': date(2023, 6, 22), 'salario': Decimal('3800.00'), 'turno': TurnoEnum.MANHA},
            {'cpf': '890.123.456-78', 'nome': 'Fernando Santos Oliveira', 'data_nascimento': date(1983, 8, 25), 'telefone_principal': '(85) 92109-8765', 'telefone_secundario': None, 'email': 'fernando.santos@email.com', 'endereco_rua': 'Rua José Vilar', 'endereco_numero': '567', 'endereco_bairro': 'Dionísio Torres', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60135-000', 'matricula': 'FUNC008', 'cargo': 'Segurança', 'data_admissao': date(2023, 7, 10), 'salario': Decimal('2200.00'), 'turno': TurnoEnum.NOITE},
            {'cpf': '901.234.567-89', 'nome': 'Juliana Costa Pereira', 'data_nascimento': date(1989, 4, 30), 'telefone_principal': '(85) 91098-7654', 'telefone_secundario': '(85) 3678-9012', 'email': 'juliana.costa@email.com', 'endereco_rua': 'Av. Dom Luís', 'endereco_numero': '890', 'endereco_bairro': 'Meireles', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60160-000', 'matricula': 'FUNC009', 'cargo': 'Pedagoga', 'data_admissao': date(2023, 8, 15), 'salario': Decimal('3600.00'), 'turno': TurnoEnum.TARDE},
            {'cpf': '012.345.678-90', 'nome': 'Marcos Vinícius Lima', 'data_nascimento': date(1986, 10, 12), 'telefone_principal': '(85) 90987-6543', 'telefone_secundario': None, 'email': 'marcos.vinicius@email.com', 'endereco_rua': 'Rua Tibúrcio Cavalcante', 'endereco_numero': '345', 'endereco_bairro': 'Meireles', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60125-000', 'matricula': 'FUNC010', 'cargo': 'Fisioterapeuta', 'data_admissao': date(2023, 9, 20), 'salario': Decimal('4100.00'), 'turno': TurnoEnum.INTEGRAL}
        ]
        
        funcionarios_criados = []
        for item in pessoas_funcionarios:
            pessoa = Pessoa(
                cpf=item['cpf'], nome=item['nome'], data_nascimento=item['data_nascimento'],
                telefone_principal=item['telefone_principal'], telefone_secundario=item['telefone_secundario'],
                email=item['email'], endereco_rua=item['endereco_rua'], endereco_numero=item['endereco_numero'],
                endereco_bairro=item['endereco_bairro'], endereco_cidade=item['endereco_cidade'],
                endereco_estado=item['endereco_estado'], endereco_cep=item['endereco_cep'], tipo_pessoa=TipoPessoa.FUNCIONARIO
            )
            db.add(pessoa)
            db.flush()
            
            funcionario = Funcionario(
                id_pessoa=pessoa.id_pessoa, matricula=item['matricula'], cargo=item['cargo'],
                data_admissao=item['data_admissao'], salario=item['salario'], turno=item['turno']
            )
            db.add(funcionario)
            funcionarios_criados.append(funcionario)
        
        db.flush()
        print(f"   {len(funcionarios_criados)} funcionários inseridos")
        
        # 3. ACOLHIDOS
        print("Inserindo acolhidos...")
        pessoas_acolhidas = [
            {'cpf': '111.222.333-44', 'nome': 'Pedro Henrique Sousa', 'data_nascimento': date(1995, 12, 3), 'telefone_principal': '(85) 94321-0987', 'telefone_secundario': None, 'endereco_rua': 'Rua da Esperança', 'endereco_numero': '111', 'endereco_bairro': 'Montese', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60425-000', 'numero_prontuario': 'PRONT001', 'data_entrada': date(2024, 1, 10), 'motivo_acolhimento': 'Situação de rua por desemprego prolongado', 'dependencia_quimica': False},
            {'cpf': '222.333.444-55', 'nome': 'Francisca Maria Jesus', 'data_nascimento': date(1980, 4, 25), 'telefone_principal': '(85) 93210-9876', 'telefone_secundario': '(85) 3567-8901', 'endereco_rua': 'Av. Bezerra de Menezes', 'endereco_numero': '222', 'endereco_bairro': 'São Gerardo', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60325-000', 'numero_prontuario': 'PRONT002', 'data_entrada': date(2024, 2, 15), 'motivo_acolhimento': 'Violência doméstica e vulnerabilidade social', 'dependencia_quimica': False},
            {'cpf': '333.444.555-66', 'nome': 'José Antonio Silva', 'data_nascimento': date(1970, 8, 14), 'telefone_principal': '(85) 92109-8765', 'telefone_secundario': None, 'endereco_rua': 'Rua Santa Clara', 'endereco_numero': '333', 'endereco_bairro': 'Parangaba', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60740-000', 'numero_prontuario': 'PRONT003', 'data_entrada': date(2024, 3, 20), 'motivo_acolhimento': 'Dependência química e abandono familiar', 'dependencia_quimica': True},
            {'cpf': '444.555.666-77', 'nome': 'Rita de Cássia Alves', 'data_nascimento': date(1987, 1, 20), 'telefone_principal': '(85) 91098-7654', 'telefone_secundario': '(85) 3678-9012', 'endereco_rua': 'Rua dos Coqueiros', 'endereco_numero': '444', 'endereco_bairro': 'Messejana', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60840-000', 'numero_prontuario': 'PRONT004', 'data_entrada': date(2024, 4, 25), 'motivo_acolhimento': 'Perda de moradia por questões financeiras', 'dependencia_quimica': False},
            {'cpf': '555.666.777-88', 'nome': 'Antônio Carlos Moura', 'data_nascimento': date(1965, 6, 12), 'telefone_principal': '(85) 90987-6543', 'telefone_secundario': None, 'endereco_rua': 'Av. Sargento Hermínio', 'endereco_numero': '555', 'endereco_bairro': 'Monte Castelo', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60325-000', 'numero_prontuario': 'PRONT005', 'data_entrada': date(2024, 5, 30), 'motivo_acolhimento': 'Situação de rua e problemas de saúde mental', 'dependencia_quimica': False},
            {'cpf': '666.777.888-99', 'nome': 'Socorro Ribeiro Santos', 'data_nascimento': date(1978, 9, 5), 'telefone_principal': '(85) 89876-5432', 'telefone_secundario': None, 'endereco_rua': 'Rua General Sampaio', 'endereco_numero': '666', 'endereco_bairro': 'Centro', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60020-000', 'numero_prontuario': 'PRONT006', 'data_entrada': date(2024, 6, 8), 'motivo_acolhimento': 'Abandono familiar e idade avançada', 'dependencia_quimica': False},
            {'cpf': '777.888.999-00', 'nome': 'Miguel dos Santos Ferreira', 'data_nascimento': date(1992, 11, 18), 'telefone_principal': '(85) 88765-4321', 'telefone_secundario': None, 'endereco_rua': 'Av. Heráclito Graça', 'endereco_numero': '777', 'endereco_bairro': 'Centro', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60140-000', 'numero_prontuario': 'PRONT007', 'data_entrada': date(2024, 7, 12), 'motivo_acolhimento': 'Egressão do sistema prisional sem apoio familiar', 'dependencia_quimica': True},
            {'cpf': '888.999.000-11', 'nome': 'Cleide Oliveira Lima', 'data_nascimento': date(1985, 3, 22), 'telefone_principal': '(85) 87654-3210', 'telefone_secundario': '(85) 3789-0123', 'endereco_rua': 'Rua Guilherme Rocha', 'endereco_numero': '888', 'endereco_bairro': 'Centro', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60030-000', 'numero_prontuario': 'PRONT008', 'data_entrada': date(2024, 8, 20), 'motivo_acolhimento': 'Violência doméstica com filhos menores', 'dependencia_quimica': False},
            {'cpf': '999.000.111-22', 'nome': 'Ronaldo Pereira Costa', 'data_nascimento': date(1968, 7, 10), 'telefone_principal': '(85) 86543-2109', 'telefone_secundario': None, 'endereco_rua': 'Rua Senador Alencar', 'endereco_numero': '999', 'endereco_bairro': 'Centro', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60050-000', 'numero_prontuario': 'PRONT009', 'data_entrada': date(2024, 9, 15), 'motivo_acolhimento': 'Desemprego e despejo por falta de pagamento', 'dependencia_quimica': False},
            {'cpf': '000.111.222-33', 'nome': 'Vera Lúcia Nascimento', 'data_nascimento': date(1975, 12, 28), 'telefone_principal': '(85) 85432-1098', 'telefone_secundario': None, 'endereco_rua': 'Av. Pessoa Anta', 'endereco_numero': '1010', 'endereco_bairro': 'Benfica', 'endereco_cidade': 'Fortaleza', 'endereco_estado': 'CE', 'endereco_cep': '60015-000', 'numero_prontuario': 'PRONT010', 'data_entrada': date(2024, 10, 5), 'motivo_acolhimento': 'Problemas de saúde mental e abandono', 'dependencia_quimica': False}
        ]
        
        acolhidos_criados = []
        for item in pessoas_acolhidas:
            pessoa = Pessoa(
                cpf=item['cpf'], nome=item['nome'], data_nascimento=item['data_nascimento'],
                telefone_principal=item['telefone_principal'], telefone_secundario=item['telefone_secundario'],
                endereco_rua=item['endereco_rua'], endereco_numero=item['endereco_numero'],
                endereco_bairro=item['endereco_bairro'], endereco_cidade=item['endereco_cidade'],
                endereco_estado=item['endereco_estado'], endereco_cep=item['endereco_cep'], tipo_pessoa=TipoPessoa.ACOLHIDO
            )
            db.add(pessoa)
            db.flush()
            
            acolhido = Acolhido(
                id_pessoa=pessoa.id_pessoa, numero_prontuario=item['numero_prontuario'],
                data_entrada=item['data_entrada'], motivo_acolhimento=item['motivo_acolhimento'],
                dependencia_quimica=item['dependencia_quimica']
            )
            db.add(acolhido)
            acolhidos_criados.append(acolhido)
        
        db.flush()
        print(f"   {len(acolhidos_criados)} acolhidos inseridos")
        
        # 4. ACOLHIMENTOS
        print("Inserindo acolhimentos...")
        acolhimentos = [
            Acolhimento(id_acolhido=1, id_abrigo=1, data_entrada=date(2024, 1, 10), numero_vaga='V001', status_ativo=True),
            Acolhimento(id_acolhido=2, id_abrigo=2, data_entrada=date(2024, 2, 15), numero_vaga='V002', status_ativo=True),
            Acolhimento(id_acolhido=3, id_abrigo=4, data_entrada=date(2024, 3, 20), numero_vaga='V003', status_ativo=True),
            Acolhimento(id_acolhido=4, id_abrigo=3, data_entrada=date(2024, 4, 25), numero_vaga='V004', status_ativo=True),
            Acolhimento(id_acolhido=5, id_abrigo=5, data_entrada=date(2024, 5, 30), numero_vaga='V005', status_ativo=True),
            Acolhimento(id_acolhido=6, id_abrigo=6, data_entrada=date(2024, 6, 8), numero_vaga='V006', status_ativo=True),
            Acolhimento(id_acolhido=7, id_abrigo=7, data_entrada=date(2024, 7, 12), numero_vaga='V007', status_ativo=True),
            Acolhimento(id_acolhido=8, id_abrigo=8, data_entrada=date(2024, 8, 20), numero_vaga='V008', status_ativo=True),
            Acolhimento(id_acolhido=9, id_abrigo=9, data_entrada=date(2024, 9, 15), numero_vaga='V009', status_ativo=True),
            Acolhimento(id_acolhido=10, id_abrigo=10, data_entrada=date(2024, 10, 5), numero_vaga='V010', status_ativo=True)
        ]
        
        for acolhimento in acolhimentos:
            db.add(acolhimento)
        db.flush()
        print(f"   {len(acolhimentos)} acolhimentos inseridos")
        
        # 5. ATENDIMENTOS
        print("Inserindo atendimentos...")
        atendimentos = [
            Atendimento(id_acolhido=1, id_funcionario=1, data_atendimento=date(2024, 1, 15), tipo_atendimento='Acolhimento', descricao='Primeira entrevista e avaliação social', observacoes='Pessoa demonstrou interesse em participar dos programas de reinserção'),
            Atendimento(id_acolhido=2, id_funcionario=2, data_atendimento=date(2024, 2, 20), tipo_atendimento='Psicológico', descricao='Sessão de acompanhamento psicológico', observacoes='Trabalhando questões relacionadas à violência sofrida'),
            Atendimento(id_acolhido=3, id_funcionario=1, data_atendimento=date(2024, 3, 25), tipo_atendimento='Social', descricao='Orientação sobre benefícios sociais', observacoes='Iniciado processo para obtenção de documentos'),
            Atendimento(id_acolhido=4, id_funcionario=3, data_atendimento=date(2024, 4, 30), tipo_atendimento='Administrativo', descricao='Reunião de planejamento individual', observacoes='Definidas metas para os próximos 3 meses'),
            Atendimento(id_acolhido=5, id_funcionario=5, data_atendimento=date(2024, 6, 5), tipo_atendimento='Saúde', descricao='Consulta de enfermagem', observacoes='Acompanhamento de medicação para hipertensão'),
            Atendimento(id_acolhido=6, id_funcionario=7, data_atendimento=date(2024, 6, 12), tipo_atendimento='Nutricional', descricao='Avaliação nutricional e orientação alimentar', observacoes='Necessita acompanhamento devido à diabetes'),
            Atendimento(id_acolhido=7, id_funcionario=2, data_atendimento=date(2024, 7, 18), tipo_atendimento='Psicológico', descricao='Atendimento para dependência química', observacoes='Encaminhado para grupo de apoio'),
            Atendimento(id_acolhido=8, id_funcionario=9, data_atendimento=date(2024, 8, 25), tipo_atendimento='Educacional', descricao='Planejamento educacional para os filhos', observacoes='Crianças matriculadas na escola próxima'),
            Atendimento(id_acolhido=9, id_funcionario=6, data_atendimento=date(2024, 9, 20), tipo_atendimento='Administrativo', descricao='Orientação sobre documentação e benefícios', observacoes='Aguardando aprovação do auxílio emergencial'),
            Atendimento(id_acolhido=10, id_funcionario=10, data_atendimento=date(2024, 10, 10), tipo_atendimento='Fisioterapia', descricao='Sessão de fisioterapia e reabilitação', observacoes='Apresentando melhora na mobilidade')
        ]
        
        for atendimento in atendimentos:
            db.add(atendimento)
        db.flush()
        print(f"   {len(atendimentos)} atendimentos inseridos")
        
        # 6. FAMILIARES
        print("Inserindo familiares...")
        familiares = [
            Familiar(id_acolhido=1, nome='Rosa Helena Sousa', parentesco='Mãe', telefone_principal='(85) 99111-2222', contato_emergencia=True),
            Familiar(id_acolhido=2, nome='Marcos Jesus Santos', parentesco='Irmão', telefone_principal='(85) 98222-3333', contato_emergencia=True),
            Familiar(id_acolhido=3, nome='Isabel Silva Costa', parentesco='Filha', telefone_principal='(85) 97333-4444', contato_emergencia=False),
            Familiar(id_acolhido=4, nome='Roberto Alves Lima', parentesco='Primo', telefone_principal='(85) 96444-5555', contato_emergencia=True),
            Familiar(id_acolhido=5, nome='Sandra Moura Oliveira', parentesco='Sobrinha', telefone_principal='(85) 95555-6666', contato_emergencia=False),
            Familiar(id_acolhido=6, nome='Francisco Ribeiro Santos', parentesco='Filho', telefone_principal='(85) 94444-7777', contato_emergencia=True),
            Familiar(id_acolhido=7, nome='Antônia Ferreira Silva', parentesco='Tia', telefone_principal='(85) 93333-8888', contato_emergencia=False),
            Familiar(id_acolhido=8, nome='João Oliveira Lima', parentesco='Irmão', telefone_principal='(85) 92222-9999', contato_emergencia=True),
            Familiar(id_acolhido=9, nome='Maria Pereira Costa', parentesco='Esposa', telefone_principal='(85) 91111-0000', contato_emergencia=True),
            Familiar(id_acolhido=10, nome='Carlos Nascimento Silva', parentesco='Filho', telefone_principal='(85) 90000-1111', contato_emergencia=False)
        ]
        
        for familiar in familiares:
            db.add(familiar)
        db.flush()
        print(f"   {len(familiares)} familiares inseridos")
        
        # Commit final
        db.commit()
        
        print("\nDADOS INSERIDOS COM SUCESSO!")
        print("="*50)
        print("RESUMO:")
        print(f"   Abrigos: {len(abrigos)}")
        print(f"   Funcionários: {len(funcionarios_criados)}")
        print(f"   Acolhidos: {len(acolhidos_criados)}")
        print(f"   Acolhimentos: {len(acolhimentos)}")
        print(f"   Atendimentos: {len(atendimentos)}")
        print(f"   Familiares: {len(familiares)}")
        print("="*50)
        print("Banco populado com sucesso!")
        
    except Exception as e:
        db.rollback()
        print(f"Erro ao inserir dados: {e}")
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    print("Populando banco de dados...")
    print("TODOS OS DADOS EXISTENTES SERAO REMOVIDOS!")
    seed_database()
    print("Processo concluído!")