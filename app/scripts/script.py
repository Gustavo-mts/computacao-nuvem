import os
from datetime import date, datetime, timedelta
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.database import engine
from app.models import (
    Pessoa, Funcionario, Acolhido, Abrigo, Acolhimento, Atendimento, Familiar,
    TipoPessoa, StatusFuncionario, StatusAcolhimento, TurnoEnum, TipoAbrigo
)

# Carregar variáveis de ambiente
load_dotenv()

# Criar sessão
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

def inserir_dados_teste():
    try:
        print("🚀 Iniciando inserção de dados de teste...")
        
        # 1. INSERIR ABRIGOS (5 registros)
        print("\nInserindo abrigos...")
        abrigos_data = [
            {
                'cnpj': '12.345.678/0001-90',
                'nome': 'Casa de Acolhimento São Francisco',
                'capacidade_total': 30,
                'endereco_rua': 'Rua das Flores, 123',
                'endereco_bairro': 'Centro',
                'endereco_cidade': 'Quixadá',
                'endereco_estado': 'CE',
                'endereco_cep': '63900-000',
                'telefone_principal': '(85) 3333-1111',
                'tipo_abrigo': TipoAbrigo.MISTO,
                'responsavel_legal': 'Maria Silva Santos',
                'ativo': True
            },
            {
                'cnpj': '23.456.789/0001-80',
                'nome': 'Abrigo Esperança',
                'capacidade_total': 25,
                'endereco_rua': 'Av. Principal, 456',
                'endereco_bairro': 'Jardim das Acácias',
                'endereco_cidade': 'Quixadá',
                'endereco_estado': 'CE',
                'endereco_cep': '63900-100',
                'telefone_principal': '(85) 3333-2222',
                'tipo_abrigo': TipoAbrigo.MASCULINO,
                'responsavel_legal': 'João Carlos Oliveira',
                'ativo': True
            },
            {
                'cnpj': '34.567.890/0001-70',
                'nome': 'Casa Lar Nossa Senhora',
                'capacidade_total': 20,
                'endereco_rua': 'Rua da Paz, 789',
                'endereco_bairro': 'São José',
                'endereco_cidade': 'Quixadá',
                'endereco_estado': 'CE',
                'endereco_cep': '63900-200',
                'telefone_principal': '(85) 3333-3333',
                'tipo_abrigo': TipoAbrigo.FEMININO,
                'responsavel_legal': 'Ana Paula Mendes',
                'ativo': True
            },
            {
                'cnpj': '45.678.901/0001-60',
                'nome': 'Abrigo Familiar Bom Jesus',
                'capacidade_total': 15,
                'endereco_rua': 'Rua dos Coqueiros, 321',
                'endereco_bairro': 'Alto Alegre',
                'endereco_cidade': 'Quixadá',
                'endereco_estado': 'CE',
                'endereco_cep': '63900-300',
                'telefone_principal': '(85) 3333-4444',
                'tipo_abrigo': TipoAbrigo.FAMILIAR,
                'responsavel_legal': 'Pedro Henrique Lima',
                'ativo': True
            },
            {
                'cnpj': '56.789.012/0001-50',
                'nome': 'Lar dos Idosos São Vicente',
                'capacidade_total': 40,
                'endereco_rua': 'Av. dos Idosos, 555',
                'endereco_bairro': 'Vila Nova',
                'endereco_cidade': 'Quixadá',
                'endereco_estado': 'CE',
                'endereco_cep': '63900-400',
                'telefone_principal': '(85) 3333-5555',
                'tipo_abrigo': TipoAbrigo.MISTO,
                'responsavel_legal': 'Francisco Almeida',
                'ativo': True
            }
        ]

        abrigos = []
        for data in abrigos_data:
            abrigo = Abrigo(**data)
            db.add(abrigo)
            abrigos.append(abrigo)
        db.commit()
        print(f"✅ {len(abrigos)} abrigos inseridos")

        # 2. INSERIR PESSOAS (10 registros - 5 funcionários e 5 acolhidos)
        print("\nInserindo pessoas...")
        pessoas_data = [
            # Funcionários
            {
                'cpf': '111.222.333-44',
                'nome': 'Carlos Eduardo Silva',
                'data_nascimento': date(1985, 5, 15),
                'telefone_principal': '(85) 98888-1111',
                'telefone_secundario': '(85) 3333-1111',
                'email': 'carlos.silva@email.com',
                'endereco_rua': 'Rua A, 100',
                'endereco_numero': '100',
                'endereco_bairro': 'Centro',
                'endereco_cidade': 'Quixadá',
                'endereco_estado': 'CE',
                'endereco_cep': '63900-000',
                'tipo_pessoa': TipoPessoa.FUNCIONARIO,
                'ativo': True
            },
            {
                'cpf': '222.333.444-55',
                'nome': 'Ana Paula Oliveira',
                'data_nascimento': date(1990, 8, 22),
                'telefone_principal': '(85) 98888-2222',
                'telefone_secundario': None,
                'email': 'ana.oliveira@email.com',
                'endereco_rua': 'Rua B, 200',
                'endereco_numero': '200',
                'endereco_bairro': 'Jardim',
                'endereco_cidade': 'Quixadá',
                'endereco_estado': 'CE',
                'endereco_cep': '63900-100',
                'tipo_pessoa': TipoPessoa.FUNCIONARIO,
                'ativo': True
            },
            # Adicione mais 3 funcionários e 5 acolhidos seguindo o mesmo padrão
            # ...
        ]

        pessoas = []
        for data in pessoas_data:
            pessoa = Pessoa(**data)
            db.add(pessoa)
            pessoas.append(pessoa)
        db.commit()
        print(f"✅ {len(pessoas)} pessoas inseridas")

        # 3. INSERIR FUNCIONÁRIOS (5 registros)
        print("\nInserindo funcionários...")
        funcionarios_data = [
            {
                'id_pessoa': pessoas[0].id_pessoa,
                'matricula': 'FUNC001',
                'cargo': 'Assistente Social',
                'data_admissao': date(2020, 1, 10),
                'salario': 3500.00,
                'turno': TurnoEnum.INTEGRAL,
                'status_funcionario': StatusFuncionario.ATIVO
            },
            {
                'id_pessoa': pessoas[1].id_pessoa,
                'matricula': 'FUNC002',
                'cargo': 'Psicólogo',
                'data_admissao': date(2021, 3, 15),
                'salario': 4200.00,
                'turno': TurnoEnum.MANHA,
                'status_funcionario': StatusFuncionario.ATIVO
            },
            # Adicione mais 3 funcionários
            # ...
        ]

        funcionarios = []
        for data in funcionarios_data:
            funcionario = Funcionario(**data)
            db.add(funcionario)
            funcionarios.append(funcionario)
        db.commit()
        print(f"✅ {len(funcionarios)} funcionários inseridos")

        # 4. INSERIR ACOLHIDOS (5 registros)
        print("\nInserindo acolhidos...")
        acolhidos_data = [
            {
                'id_pessoa': pessoas[5].id_pessoa,  # Supondo que as pessoas 5-9 são acolhidos
                'numero_prontuario': 'PRONT001',
                'data_entrada': date(2023, 1, 5),
                'data_saida': None,
                'motivo_acolhimento': 'Situação de rua',
                'dependencia_quimica': False,
                'status_acolhimento': StatusAcolhimento.ATIVO
            },
            {
                'id_pessoa': pessoas[6].id_pessoa,
                'numero_prontuario': 'PRONT002',
                'data_entrada': date(2023, 2, 10),
                'data_saida': date(2023, 6, 15),
                'motivo_acolhimento': 'Violência doméstica',
                'dependencia_quimica': True,
                'status_acolhimento': StatusAcolhimento.DESLIGADO
            },
            # Adicione mais 3 acolhidos
            # ...
        ]

        acolhidos = []
        for data in acolhidos_data:
            acolhido = Acolhido(**data)
            db.add(acolhido)
            acolhidos.append(acolhido)
        db.commit()
        print(f"✅ {len(acolhidos)} acolhidos inseridos")

        # 5. INSERIR ACOLHIMENTOS (5 registros)
        print("\nInserindo acolhimentos...")
        acolhimentos_data = [
            {
                'id_acolhido': acolhidos[0].id_acolhido,
                'id_abrigo': abrigos[0].id_abrigo,
                'data_entrada': date(2023, 1, 5),
                'data_saida': None,
                'numero_vaga': 'VAGA001',
                'status_ativo': True
            },
            {
                'id_acolhido': acolhidos[1].id_acolhido,
                'id_abrigo': abrigos[1].id_abrigo,
                'data_entrada': date(2023, 2, 10),
                'data_saida': date(2023, 6, 15),
                'numero_vaga': 'VAGA002',
                'status_ativo': False
            },
            # Adicione mais 3 acolhimentos
            # ...
        ]

        acolhimentos = []
        for data in acolhimentos_data:
            acolhimento = Acolhimento(**data)
            db.add(acolhimento)
            acolhimentos.append(acolhimento)
        db.commit()
        print(f"✅ {len(acolhimentos)} acolhimentos inseridos")

        # 6. INSERIR FAMILIARES (5 registros)
        print("\nInserindo familiares...")
        familiares_data = [
            {
                'id_acolhido': acolhidos[0].id_acolhido,
                'nome': 'Maria Silva',
                'parentesco': 'Mãe',
                'telefone_principal': '(85) 98888-9999',
                'contato_emergencia': True
            },
            {
                'id_acolhido': acolhidos[1].id_acolhido,
                'nome': 'José Oliveira',
                'parentesco': 'Irmão',
                'telefone_principal': '(85) 97777-8888',
                'contato_emergencia': False
            },
            # Adicione mais 3 familiares
            # ...
        ]

        familiares = []
        for data in familiares_data:
            familiar = Familiar(**data)
            db.add(familiar)
            familiares.append(familiar)
        db.commit()
        print(f"{len(familiares)} familiares inseridos")

        # 7. INSERIR ATENDIMENTOS (5 registros)
        print("\nInserindo atendimentos...")
        atendimentos_data = [
            {
                'id_acolhido': acolhidos[0].id_acolhido,
                'id_funcionario': funcionarios[0].id_funcionario,
                'data_atendimento': date(2023, 1, 10),
                'tipo_atendimento': 'Acolhimento inicial',
                'descricao': 'Primeiro atendimento para avaliação das necessidades',
                'observacoes': 'Necessita de acompanhamento psicológico'
            },
            {
                'id_acolhido': acolhidos[1].id_acolhido,
                'id_funcionario': funcionarios[1].id_funcionario,
                'data_atendimento': date(2023, 2, 15),
                'tipo_atendimento': 'Acompanhamento psicológico',
                'descricao': 'Sessão de terapia semanal',
                'observacoes': 'Progresso significativo no tratamento'
            },
            # Adicione mais 3 atendimentos
            # ...
        ]

        atendimentos = []
        for data in atendimentos_data:
            atendimento = Atendimento(**data)
            db.add(atendimento)
            atendimentos.append(atendimento)
        db.commit()
        print(f"{len(atendimentos)} atendimentos inseridos")

        print("\n🎉 Todos os dados de teste foram inseridos com sucesso!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao inserir dados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    inserir_dados_teste()