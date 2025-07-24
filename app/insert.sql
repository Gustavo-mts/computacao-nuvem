
DELETE FROM atendimentos;
DELETE FROM familiares;
DELETE FROM acolhimentos;
DELETE FROM funcionarios;
DELETE FROM acolhidos;
DELETE FROM pessoas;
DELETE FROM abrigos;


ALTER SEQUENCE pessoas_id_pessoa_seq RESTART WITH 1;
ALTER SEQUENCE abrigos_id_abrigo_seq RESTART WITH 1;
ALTER SEQUENCE funcionarios_id_funcionario_seq RESTART WITH 1;
ALTER SEQUENCE acolhidos_id_acolhido_seq RESTART WITH 1;
ALTER SEQUENCE acolhimentos_id_acolhimento_seq RESTART WITH 1;
ALTER SEQUENCE atendimentos_id_atendimento_seq RESTART WITH 1;
ALTER SEQUENCE familiares_id_familiar_seq RESTART WITH 1;


INSERT INTO abrigos (cnpj, nome, capacidade_total, endereco_rua, endereco_numero, endereco_bairro, endereco_cidade, endereco_estado, endereco_cep, telefone_principal, tipo_abrigo, responsavel_legal, ativo) VALUES
('12.345.678/0001-90', 'Casa de Acolhimento São Francisco', 30, 'Rua São Francisco', '100', 'Centro', 'Fortaleza', 'CE', '60000-001', '(85) 3234-1000', 'MASCULINO', 'Padre João Silva', TRUE),
('23.456.789/0001-01', 'Lar Feminino Santa Clara', 25, 'Av. da Universidade', '200', 'Benfica', 'Fortaleza', 'CE', '60020-001', '(85) 3234-2000', 'FEMININO', 'Irmã Maria José', TRUE),
('34.567.890/0001-12', 'Abrigo Familiar Esperança', 40, 'Rua da Harmonia', '300', 'Aldeota', 'Fortaleza', 'CE', '60150-001', '(85) 3234-3000', 'FAMILIAR', 'Dr. Carlos Mendes', TRUE),
('45.678.901/0001-23', 'Casa Mista Vida Nova', 35, 'Av. Washington Soares', '400', 'Edson Queiroz', 'Fortaleza', 'CE', '60811-001', '(85) 3234-4000', 'MISTO', 'Dra. Ana Beatriz', TRUE),
('56.789.012/0001-34', 'Abrigo Masculino Recomeço', 28, 'Rua Coronel Correia', '500', 'José Bonifácio', 'Fortaleza', 'CE', '60055-001', '(85) 3234-5000', 'MASCULINO', 'Pastor Marcos Lima', TRUE),
('67.890.123/0001-45', 'Casa Feminina Amor e Paz', 32, 'Rua Santa Teresinha', '600', 'Messejana', 'Fortaleza', 'CE', '60840-001', '(85) 3234-6000', 'FEMININO', 'Dra. Tereza Santos', TRUE),
('78.901.234/0001-56', 'Abrigo Misto Solidariedade', 45, 'Av. Alberto Magno', '700', 'Maraponga', 'Fortaleza', 'CE', '60710-001', '(85) 3234-7000', 'MISTO', 'Sr. Roberto Alves', TRUE),
('89.012.345/0001-67', 'Casa Familiar Novo Horizonte', 38, 'Rua João Cordeiro', '800', 'Cocó', 'Fortaleza', 'CE', '60192-001', '(85) 3234-8000', 'FAMILIAR', 'Sra. Lúcia Fernandes', TRUE),
('90.123.456/0001-78', 'Abrigo Masculino São José', 42, 'Rua Major Facundo', '900', 'Centro', 'Fortaleza', 'CE', '60025-001', '(85) 3234-9000', 'MASCULINO', 'Frei Antonio Carlos', TRUE),
('01.234.567/0001-89', 'Lar Misto Fraternidade', 50, 'Av. Desembargador Moreira', '1000', 'Aldeota', 'Fortaleza', 'CE', '60170-001', '(85) 3234-0100', 'MISTO', 'Dr. Fernando Costa', TRUE);


INSERT INTO pessoas (cpf, nome, data_nascimento, telefone_principal, telefone_secundario, email, endereco_rua, endereco_numero, endereco_bairro, endereco_cidade, endereco_estado, endereco_cep, tipo_pessoa, ativo) VALUES
('123.456.789-01', 'Maria Silva Santos', '1985-03-15', '(85) 98765-4321', '(85) 3234-5678', 'maria.silva@email.com', 'Rua das Flores', '123', 'Centro', 'Fortaleza', 'CE', '60000-000', 'FUNCIONARIO', TRUE),
('234.567.890-12', 'João Carlos Oliveira', '1990-07-22', '(85) 99876-5432', NULL, 'joao.carlos@email.com', 'Av. Beira Mar', '456', 'Mucuripe', 'Fortaleza', 'CE', '60165-000', 'FUNCIONARIO', TRUE),
('345.678.901-23', 'Ana Paula Costa', '1988-11-30', '(85) 97654-3210', '(85) 3345-6789', 'ana.paula@email.com', 'Rua do Sol', '789', 'Aldeota', 'Fortaleza', 'CE', '60150-000', 'FUNCIONARIO', TRUE),
('456.789.012-34', 'Carlos Roberto Lima', '1975-05-10', '(85) 96543-2109', NULL, 'carlos.lima@email.com', 'Rua da Paz', '321', 'Benfica', 'Fortaleza', 'CE', '60020-000', 'FUNCIONARIO', TRUE),
('567.890.123-45', 'Luciana Ferreira', '1992-09-18', '(85) 95432-1098', '(85) 3456-7890', 'luciana.ferreira@email.com', 'Av. Santos Dumont', '654', 'Papicu', 'Fortaleza', 'CE', '60175-000', 'FUNCIONARIO', TRUE),
('678.901.234-56', 'Ricardo Mendes Silva', '1987-12-08', '(85) 94321-0987', NULL, 'ricardo.mendes@email.com', 'Rua Barão de Studart', '987', 'Meireles', 'Fortaleza', 'CE', '60160-000', 'FUNCIONARIO', TRUE),
('789.012.345-67', 'Patricia Rocha Alves', '1991-02-14', '(85) 93210-9876', '(85) 3567-8901', 'patricia.rocha@email.com', 'Av. Pontes Vieira', '1234', 'São Gerardo', 'Fortaleza', 'CE', '60325-000', 'FUNCIONARIO', TRUE),
('890.123.456-78', 'Fernando Santos Oliveira', '1983-08-25', '(85) 92109-8765', NULL, 'fernando.santos@email.com', 'Rua José Vilar', '567', 'Dionísio Torres', 'Fortaleza', 'CE', '60135-000', 'FUNCIONARIO', TRUE),
('901.234.567-89', 'Juliana Costa Pereira', '1989-04-30', '(85) 91098-7654', '(85) 3678-9012', 'juliana.costa@email.com', 'Av. Dom Luís', '890', 'Meireles', 'Fortaleza', 'CE', '60160-000', 'FUNCIONARIO', TRUE),
('012.345.678-90', 'Marcos Vinícius Lima', '1986-10-12', '(85) 90987-6543', NULL, 'marcos.vinicius@email.com', 'Rua Tibúrcio Cavalcante', '345', 'Meireles', 'Fortaleza', 'CE', '60125-000', 'FUNCIONARIO', TRUE);


INSERT INTO funcionarios (id_pessoa, matricula, cargo, data_admissao, salario, turno, status_funcionario) VALUES
(1, 'FUNC001', 'Assistente Social', '2023-01-15', 3500.00, 'MANHA', 'ATIVO'),
(2, 'FUNC002', 'Psicólogo', '2023-02-20', 4000.00, 'TARDE', 'ATIVO'),
(3, 'FUNC003', 'Coordenadora', '2022-06-10', 5500.00, 'INTEGRAL', 'ATIVO'),
(4, 'FUNC004', 'Educador Social', '2023-03-05', 2800.00, 'NOITE', 'ATIVO'),
(5, 'FUNC005', 'Enfermeira', '2023-04-12', 4200.00, 'MANHA', 'ATIVO'),
(6, 'FUNC006', 'Administrador', '2023-05-18', 4500.00, 'TARDE', 'ATIVO'),
(7, 'FUNC007', 'Nutricionista', '2023-06-22', 3800.00, 'MANHA', 'ATIVO'),
(8, 'FUNC008', 'Segurança', '2023-07-10', 2200.00, 'NOITE', 'ATIVO'),
(9, 'FUNC009', 'Pedagoga', '2023-08-15', 3600.00, 'TARDE', 'ATIVO'),
(10, 'FUNC010', 'Fisioterapeuta', '2023-09-20', 4100.00, 'INTEGRAL', 'ATIVO');


INSERT INTO pessoas (cpf, nome, data_nascimento, telefone_principal, telefone_secundario, email, endereco_rua, endereco_numero, endereco_bairro, endereco_cidade, endereco_estado, endereco_cep, tipo_pessoa, ativo) VALUES
('111.222.333-44', 'Pedro Henrique Sousa', '1995-12-03', '(85) 94321-0987', NULL, NULL, 'Rua da Esperança', '111', 'Montese', 'Fortaleza', 'CE', '60425-000', 'ACOLHIDO', TRUE),
('222.333.444-55', 'Francisca Maria Jesus', '1980-04-25', '(85) 93210-9876', '(85) 3567-8901', NULL, 'Av. Bezerra de Menezes', '222', 'São Gerardo', 'Fortaleza', 'CE', '60325-000', 'ACOLHIDO', TRUE),
('333.444.555-66', 'José Antonio Silva', '1970-08-14', '(85) 92109-8765', NULL, NULL, 'Rua Santa Clara', '333', 'Parangaba', 'Fortaleza', 'CE', '60740-000', 'ACOLHIDO', TRUE),
('444.555.666-77', 'Rita de Cássia Alves', '1987-01-20', '(85) 91098-7654', '(85) 3678-9012', NULL, 'Rua dos Coqueiros', '444', 'Messejana', 'Fortaleza', 'CE', '60840-000', 'ACOLHIDO', TRUE),
('555.666.777-88', 'Antônio Carlos Moura', '1965-06-12', '(85) 90987-6543', NULL, NULL, 'Av. Sargento Hermínio', '555', 'Monte Castelo', 'Fortaleza', 'CE', '60325-000', 'ACOLHIDO', TRUE),
('666.777.888-99', 'Socorro Ribeiro Santos', '1978-09-05', '(85) 89876-5432', NULL, NULL, 'Rua General Sampaio', '666', 'Centro', 'Fortaleza', 'CE', '60020-000', 'ACOLHIDO', TRUE),
('777.888.999-00', 'Miguel dos Santos Ferreira', '1992-11-18', '(85) 88765-4321', NULL, NULL, 'Av. Heráclito Graça', '777', 'Centro', 'Fortaleza', 'CE', '60140-000', 'ACOLHIDO', TRUE),
('888.999.000-11', 'Cleide Oliveira Lima', '1985-03-22', '(85) 87654-3210', '(85) 3789-0123', NULL, 'Rua Guilherme Rocha', '888', 'Centro', 'Fortaleza', 'CE', '60030-000', 'ACOLHIDO', TRUE),
('999.000.111-22', 'Ronaldo Pereira Costa', '1968-07-10', '(85) 86543-2109', NULL, NULL, 'Rua Senador Alencar', '999', 'Centro', 'Fortaleza', 'CE', '60050-000', 'ACOLHIDO', TRUE),
('000.111.222-33', 'Vera Lúcia Nascimento', '1975-12-28', '(85) 85432-1098', NULL, NULL, 'Av. Pessoa Anta', '1010', 'Benfica', 'Fortaleza', 'CE', '60015-000', 'ACOLHIDO', TRUE);


INSERT INTO acolhidos (id_pessoa, numero_prontuario, data_entrada, data_saida, motivo_acolhimento, dependencia_quimica, status_acolhimento) VALUES
(11, 'PRONT001', '2024-01-10', NULL, 'Situação de rua por desemprego prolongado', FALSE, 'ATIVO'),
(12, 'PRONT002', '2024-02-15', NULL, 'Violência doméstica e vulnerabilidade social', FALSE, 'ATIVO'),
(13, 'PRONT003', '2024-03-20', NULL, 'Dependência química e abandono familiar', TRUE, 'ATIVO'),
(14, 'PRONT004', '2024-04-25', NULL, 'Perda de moradia por questões financeiras', FALSE, 'ATIVO'),
(15, 'PRONT005', '2024-05-30', NULL, 'Situação de rua e problemas de saúde mental', FALSE, 'ATIVO'),
(16, 'PRONT006', '2024-06-08', NULL, 'Abandono familiar e idade avançada', FALSE, 'ATIVO'),
(17, 'PRONT007', '2024-07-12', NULL, 'Egressão do sistema prisional sem apoio familiar', TRUE, 'ATIVO'),
(18, 'PRONT008', '2024-08-20', NULL, 'Violência doméstica com filhos menores', FALSE, 'ATIVO'),
(19, 'PRONT009', '2024-09-15', NULL, 'Desemprego e despejo por falta de pagamento', FALSE, 'ATIVO'),
(20, 'PRONT010', '2024-10-05', NULL, 'Problemas de saúde mental e abandono', FALSE, 'ATIVO');


INSERT INTO acolhimentos (id_acolhido, id_abrigo, data_entrada, data_saida, numero_vaga, status_ativo) VALUES
(1, 1, '2024-01-10', NULL, 'V001', TRUE),  -- Pedro no São Francisco (masculino)
(2, 2, '2024-02-15', NULL, 'V002', TRUE),  -- Francisca no Santa Clara (feminino)
(3, 4, '2024-03-20', NULL, 'V003', TRUE),  -- José na Vida Nova (misto)
(4, 3, '2024-04-25', NULL, 'V004', TRUE),  -- Rita na Esperança (familiar)
(5, 5, '2024-05-30', NULL, 'V005', TRUE),  -- Antônio no Recomeço (masculino)
(6, 6, '2024-06-08', NULL, 'V006', TRUE),  -- Socorro na Amor e Paz (feminino)
(7, 7, '2024-07-12', NULL, 'V007', TRUE),  -- Miguel na Solidariedade (misto)
(8, 8, '2024-08-20', NULL, 'V008', TRUE),  -- Cleide no Novo Horizonte (familiar)
(9, 9, '2024-09-15', NULL, 'V009', TRUE),  -- Ronaldo no São José (masculino)
(10, 10, '2024-10-05', NULL, 'V010', TRUE); -- Vera na Fraternidade (misto)


INSERT INTO atendimentos (id_acolhido, id_funcionario, data_atendimento, tipo_atendimento, descricao, observacoes) VALUES
(1, 1, '2024-01-15', 'Acolhimento', 'Primeira entrevista e avaliação social', 'Pessoa demonstrou interesse em participar dos programas de reinserção'),
(2, 2, '2024-02-20', 'Psicológico', 'Sessão de acompanhamento psicológico', 'Trabalhando questões relacionadas à violência sofrida'),
(3, 1, '2024-03-25', 'Social', 'Orientação sobre benefícios sociais', 'Iniciado processo para obtenção de documentos'),
(4, 3, '2024-04-30', 'Administrativo', 'Reunião de planejamento individual', 'Definidas metas para os próximos 3 meses'),
(5, 5, '2024-06-05', 'Saúde', 'Consulta de enfermagem', 'Acompanhamento de medicação para hipertensão'),
(6, 7, '2024-06-12', 'Nutricional', 'Avaliação nutricional e orientação alimentar', 'Necessita acompanhamento devido à diabetes'),
(7, 2, '2024-07-18', 'Psicológico', 'Atendimento para dependência química', 'Encaminhado para grupo de apoio'),
(8, 9, '2024-08-25', 'Educacional', 'Planejamento educacional para os filhos', 'Crianças matriculadas na escola próxima'),
(9, 6, '2024-09-20', 'Administrativo', 'Orientação sobre documentação e benefícios', 'Aguardando aprovação do auxílio emergencial'),
(10, 10, '2024-10-10', 'Fisioterapia', 'Sessão de fisioterapia e reabilitação', 'Apresentando melhora na mobilidade');


INSERT INTO familiares (id_acolhido, nome, parentesco, telefone_principal, contato_emergencia) VALUES
(1, 'Rosa Helena Sousa', 'Mãe', '(85) 99111-2222', TRUE),
(2, 'Marcos Jesus Santos', 'Irmão', '(85) 98222-3333', TRUE),
(3, 'Isabel Silva Costa', 'Filha', '(85) 97333-4444', FALSE),
(4, 'Roberto Alves Lima', 'Primo', '(85) 96444-5555', TRUE),
(5, 'Sandra Moura Oliveira', 'Sobrinha', '(85) 95555-6666', FALSE),
(6, 'Francisco Ribeiro Santos', 'Filho', '(85) 94444-7777', TRUE),
(7, 'Antônia Ferreira Silva', 'Tia', '(85) 93333-8888', FALSE),
(8, 'João Oliveira Lima', 'Irmão', '(85) 92222-9999', TRUE),
(9, 'Maria Pereira Costa', 'Esposa', '(85) 91111-0000', TRUE),
(10, 'Carlos Nascimento Silva', 'Filho', '(85) 90000-1111', FALSE);


SELECT 'Abrigos' as tabela, COUNT(*) as total FROM abrigos
UNION ALL
SELECT 'Pessoas', COUNT(*) FROM pessoas
UNION ALL
SELECT 'Funcionários', COUNT(*) FROM funcionarios
UNION ALL
SELECT 'Acolhidos', COUNT(*) FROM acolhidos
UNION ALL
SELECT 'Acolhimentos', COUNT(*) FROM acolhimentos
UNION ALL
SELECT 'Atendimentos', COUNT(*) FROM atendimentos
UNION ALL
SELECT 'Familiares', COUNT(*) FROM familiares;


SELECT 'Dados inseridos com sucesso! Total: 60 registros' as resultado;