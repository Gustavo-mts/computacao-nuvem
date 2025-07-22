"""
Sistema de Gestão para Abrigos
Script principal para inicialização e teste do sistema
"""

from sqlalchemy.orm import Session
from app import database, crud, models, schemas
from datetime import date
from app.models import TipoAbrigo, TurnoEnum


def main():
    """Inicializa o sistema e cria dados básicos para teste"""
    
    # Conectar ao banco de dados
    db: Session = database.SessionLocal()
    
    try:
        # Criar tabelas no banco de dados
        models.Base.metadata.create_all(bind=database.engine)
        print("Tabelas do banco de dados criadas/verificadas com sucesso.")
        
        # Criar abrigo padrão
        print("Verificando abrigo padrão...")
        if not crud.buscar_abrigo_por_nome(db, "Abrigo Central"):
            crud.criar_abrigo(db, schemas.AbrigoCreate(
                nome="Abrigo Central",
                localizacao="Centro de São Paulo",
                tipo=TipoAbrigo.MISTO,
                capacidade=100,
                cnpj="12.345.678/0001-90",
                endereco_rua="Rua Central, 100",
                endereco_bairro="Centro",
                endereco_cidade="São Paulo",
                endereco_estado="SP",
                telefone_principal="11933334444",
                responsavel_legal="Maria Silva Santos"
            ))
            print("Abrigo Central criado com sucesso.")
        else:
            print("Abrigo Central já existe no sistema.")

        # Criar funcionário coordenador
        print("Verificando funcionário coordenador...")
        if not crud.buscar_funcionario_por_matricula(db, "FUNC001"):
            crud.criar_funcionario(db, schemas.FuncionarioCreate(
                nome="Carlos Eduardo Silva",
                cpf="12345678900",
                data_nascimento=date(1985, 5, 15),
                telefone="11999999999",
                cargo="Coordenador Geral",
                turno=TurnoEnum.INTEGRAL,
                matricula="FUNC001",
                endereco_rua="Rua dos Funcionários, 200",
                endereco_bairro="Vila Madalena",
                endereco_cidade="São Paulo",
                endereco_estado="SP",
                data_admissao=date.today(),
                salario=4500.00,
                email="carlos.silva@abrigo.org"
            ))
            print("Funcionário coordenador criado com sucesso.")
        else:
            print("Funcionário FUNC001 já existe no sistema.")

        # Criar profissional de saúde
        print("Verificando profissional de saúde...")
        if not crud.buscar_profissional_por_registro(db, "CRP001"):
            crud.criar_profissional_saude(db, schemas.ProfissionalSaudeCreate(
                nome="Dra. Ana Beatriz Lima",
                cpf="98765432100",
                data_nascimento=date(1990, 7, 20),
                telefone="11888888888",
                area="Psicologia",
                registro="CRP001",
                endereco_rua="Rua da Saúde, 300",
                endereco_bairro="Consolação",
                endereco_cidade="São Paulo",
                endereco_estado="SP",
                email="ana.lima@abrigo.org"
            ))
            print("Profissional de saúde criado com sucesso.")
        else:
            print("Profissional CRP001 já existe no sistema.")

        # Criar pessoa para acolhimento
        print("Verificando pessoa para acolhimento...")
        if not crud.buscar_pessoa_por_cpf(db, "11122233344"):
            crud.criar_pessoa_acolhida(db, schemas.PessoaAcolhidaCreate(
                nome="João dos Santos Silva",
                cpf="11122233344",
                data_nascimento=date(1975, 3, 10),
                historico_saude="Hipertensão controlada",
                genero="Masculino",
                necessidade_especial=False,
                telefone_principal="11955556666",
                endereco_rua="Rua Sem Nome, s/n",
                endereco_bairro="Centro",
                endereco_cidade="São Paulo",
                endereco_estado="SP",
                motivo_acolhimento="Situação de rua decorrente de desemprego prolongado",
                numero_prontuario="PRONT001"
            ))
            print("Pessoa acolhida cadastrada com sucesso.")
        else:
            print("Pessoa com CPF 11122233344 já existe no sistema.")

        # Registrar admissão
        print("Verificando admissão ativa...")
        pessoa = crud.buscar_pessoa_por_cpf(db, "11122233344")
        abrigo = crud.buscar_abrigo_por_nome(db, "Abrigo Central")
        
        if not crud.buscar_admissao_ativa_por_pessoa(db, pessoa.id_pessoa):
            # Localizar acolhido correspondente
            acolhido = db.query(models.Acolhido).filter(
                models.Acolhido.id_pessoa == pessoa.id_pessoa
            ).first()
            
            if acolhido:
                crud.registrar_admissao(db, schemas.AdmissaoCreate(
                    pessoa_id=acolhido.id_acolhido,
                    abrigo_id=abrigo.id_abrigo,
                    data_admissao=date.today(),
                    numero_vaga="V001"
                ))
                print("Admissão registrada com sucesso.")
            else:
                print("Erro: Acolhido não encontrado para a pessoa especificada.")
        else:
            print("Pessoa já possui admissão ativa no sistema.")

        # Exibir relatório do sistema
        print("\n" + "="*50)
        print("RELATÓRIO DO SISTEMA")
        print("="*50)
        
        admissoes = crud.listar_admissoes(db)
        for admissao in admissoes:
            acolhido = db.query(models.Acolhido).filter(
                models.Acolhido.id_acolhido == admissao.id_acolhido
            ).first()
            
            if acolhido and acolhido.pessoa:
                status = "Ativa" if admissao.status_ativo else "Finalizada"
                print(f"Pessoa: {acolhido.pessoa.nome}")
                print(f"Abrigo: {admissao.abrigo.nome}")
                print(f"Data de Entrada: {admissao.data_entrada}")
                print(f"Status: {status}")
                print("-" * 30)

        # Estatísticas finais
        print("\nESTATÍSTICAS DO SISTEMA:")
        print(f"Total de Funcionários: {len(crud.listar_funcionarios(db))}")
        print(f"Total de Abrigos: {len(crud.listar_abrigos(db))}")
        print(f"Total de Admissões: {len(admissoes)}")
        print(f"Admissões Ativas: {len([a for a in admissoes if a.status_ativo])}")
        
        print("\nSistema inicializado com sucesso.")

    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
        db.rollback()
        
        # Log detalhado do erro em ambiente de desenvolvimento
        import traceback
        print("\nDetalhes do erro:")
        traceback.print_exc()
        
    finally:
        db.close()


if __name__ == "__main__":
    main()