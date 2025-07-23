import os
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime
from app.database import engine
from app.models import Abrigo, TipoAbrigo

# Carregar variáveis de ambiente
load_dotenv()

# Criar sessão
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

def inserir_abrigos():
    try:
        print("🚀 Iniciando inserção de abrigos...")
        
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
            },
            {
                'cnpj': '67.890.123/0001-40',
                'nome': 'Abrigo Nova Vida',
                'capacidade_total': 35,
                'endereco_rua': 'Rua Nova Esperança, 666',
                'endereco_bairro': 'Bela Vista',
                'endereco_cidade': 'Quixadá',
                'endereco_estado': 'CE',
                'endereco_cep': '63900-500',
                'telefone_principal': '(85) 3333-6666',
                'tipo_abrigo': TipoAbrigo.MASCULINO,
                'responsavel_legal': 'Roberto Souza',
                'ativo': True
            },
            {
                'cnpj': '78.901.234/0001-30',
                'nome': 'Lar da Criança Feliz',
                'capacidade_total': 50,
                'endereco_rua': 'Av. da Criança, 777',
                'endereco_bairro': 'Vila Feliz',
                'endereco_cidade': 'Quixadá',
                'endereco_estado': 'CE',
                'endereco_cep': '63900-600',
                'telefone_principal': '(85) 3333-7777',
                'tipo_abrigo': TipoAbrigo.FAMILIAR,
                'responsavel_legal': 'Carla Ribeiro',
                'ativo': True
            },
            {
                'cnpj': '89.012.345/0001-20',
                'nome': 'Abrigo Sol Nascente',
                'capacidade_total': 28,
                'endereco_rua': 'Rua do Sol, 888',
                'endereco_bairro': 'Sol Poente',
                'endereco_cidade': 'Quixadá',
                'endereco_estado': 'CE',
                'endereco_cep': '63900-700',
                'telefone_principal': '(85) 3333-8888',
                'tipo_abrigo': TipoAbrigo.FEMININO,
                'responsavel_legal': 'Lucia Ferreira',
                'ativo': True
            },
            {
                'cnpj': '90.123.456/0001-10',
                'nome': 'Casa de Passagem Amanhecer',
                'capacidade_total': 18,
                'endereco_rua': 'Rua do Amanhecer, 999',
                'endereco_bairro': 'Novo Horizonte',
                'endereco_cidade': 'Quixadá',
                'endereco_estado': 'CE',
                'endereco_cep': '63900-800',
                'telefone_principal': '(85) 3333-9999',
                'tipo_abrigo': TipoAbrigo.MISTO,
                'responsavel_legal': 'Marcos Aurélio',
                'ativo': True
            },
            {
                'cnpj': '01.234.567/0001-00',
                'nome': 'Abrigo Esperança II',
                'capacidade_total': 22,
                'endereco_rua': 'Av. da Esperança, 1000',
                'endereco_bairro': 'Esperança Nova',
                'endereco_cidade': 'Quixadá',
                'endereco_estado': 'CE',
                'endereco_cep': '63900-900',
                'telefone_principal': '(85) 3333-0000',
                'tipo_abrigo': TipoAbrigo.MASCULINO,
                'responsavel_legal': 'Antônio Carlos',
                'ativo': True
            }
        ]

        for data in abrigos_data:
            abrigo = Abrigo(**data)
            db.add(abrigo)
        
        db.commit()
        print(f"✅ {len(abrigos_data)} abrigos inseridos com sucesso!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao inserir abrigos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    inserir_abrigos()