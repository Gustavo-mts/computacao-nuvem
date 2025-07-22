from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import database, crud, models, schemas
from app.models import TipoAbrigo, TurnoEnum, Acolhimento
from datetime import date
from typing import Optional

app = FastAPI(
    title="Sistema de Gestão para Abrigos",
    description="Interface web para gerenciar abrigos e pessoas em situação de vulnerabilidade",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():
    models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    total_abrigos = len(crud.listar_abrigos(db))
    total_funcionarios = len(crud.listar_funcionarios(db))
    total_admissoes = len(crud.listar_admissoes(db, ativas=True))
    
    abrigos_recentes = crud.listar_abrigos(db)[:3]
    funcionarios_recentes = crud.listar_funcionarios(db)[:3]
    admissoes_recentes = crud.listar_admissoes(db)[:5]
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_abrigos": total_abrigos,
        "total_funcionarios": total_funcionarios,
        "total_admissoes": total_admissoes,
        "abrigos_recentes": abrigos_recentes,
        "funcionarios_recentes": funcionarios_recentes,
        "admissoes_recentes": admissoes_recentes
    })


@app.get("/abrigos", response_class=HTMLResponse)
async def listar_abrigos_page(request: Request, db: Session = Depends(get_db)):
    abrigos = crud.listar_abrigos(db)
    return templates.TemplateResponse("abrigos.html", {
        "request": request,
        "abrigos": abrigos
    })


@app.get("/funcionarios", response_class=HTMLResponse)
async def listar_funcionarios_page(request: Request, db: Session = Depends(get_db)):
    funcionarios = crud.listar_funcionarios(db)
    return templates.TemplateResponse("funcionarios.html", {
        "request": request,
        "funcionarios": funcionarios
    })


@app.get("/admissoes", response_class=HTMLResponse)
async def listar_admissoes_page(request: Request, db: Session = Depends(get_db)):
    admissoes = crud.listar_admissoes(db)
    return templates.TemplateResponse("admissoes.html", {
        "request": request,
        "admissoes": admissoes
    })


@app.get("/abrigos/novo", response_class=HTMLResponse)
async def novo_abrigo_form(request: Request):
    return templates.TemplateResponse("novo_abrigo.html", {
        "request": request,
        "tipos_abrigo": [t.value for t in TipoAbrigo]
    })


@app.post("/abrigos/criar")
async def criar_abrigo_form(
    request: Request,
    nome: str = Form(...),
    cnpj: str = Form(...),
    capacidade: int = Form(...),
    endereco_rua: str = Form(...),
    endereco_bairro: str = Form(...),
    endereco_cidade: str = Form(...),
    endereco_estado: str = Form(...),
    telefone: str = Form(...),
    tipo: str = Form(...),
    responsavel: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        abrigo_data = schemas.AbrigoCreate(
            nome=nome,
            localizacao=f"{endereco_cidade}, {endereco_estado}",
            tipo=TipoAbrigo(tipo),
            capacidade=capacidade,
            cnpj=cnpj,
            endereco_rua=endereco_rua,
            endereco_bairro=endereco_bairro,
            endereco_cidade=endereco_cidade,
            endereco_estado=endereco_estado,
            telefone_principal=telefone,
            responsavel_legal=responsavel
        )
        crud.criar_abrigo(db, abrigo_data)
        return RedirectResponse(url="/abrigos", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("erro.html", {
            "request": request,
            "erro": f"Erro ao criar abrigo: {str(e)}"
        })


@app.get("/funcionarios/novo", response_class=HTMLResponse)
async def novo_funcionario_form(request: Request):
    return templates.TemplateResponse("novo_funcionario.html", {
        "request": request,
        "turnos": [t.value for t in TurnoEnum]
    })


@app.post("/funcionarios/criar")
async def criar_funcionario_form(
    request: Request,
    nome: str = Form(...),
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    telefone: str = Form(...),
    email: str = Form(""),
    endereco_rua: str = Form(...),
    endereco_bairro: str = Form(...),
    endereco_cidade: str = Form(...),
    endereco_estado: str = Form(...),
    matricula: str = Form(...),
    cargo: str = Form(...),
    salario: float = Form(...),
    turno: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        funcionario_data = schemas.FuncionarioCreate(
            nome=nome,
            cpf=cpf,
            data_nascimento=date.fromisoformat(data_nascimento),
            telefone=telefone,
            cargo=cargo,
            turno=TurnoEnum(turno),
            matricula=matricula,
            endereco_rua=endereco_rua,
            endereco_bairro=endereco_bairro,
            endereco_cidade=endereco_cidade,
            endereco_estado=endereco_estado,
            data_admissao=date.today(),
            salario=salario,
            email=email if email else None
        )
        crud.criar_funcionario(db, funcionario_data)
        return RedirectResponse(url="/funcionarios", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("erro.html", {
            "request": request,
            "erro": f"Erro ao criar funcionário: {str(e)}"
        })


@app.get("/admissoes/nova", response_class=HTMLResponse)
async def nova_admissao_form(request: Request, db: Session = Depends(get_db)):
    try:
        acolhidos_disponiveis = []
        all_acolhidos = crud.listar_acolhidos(db, ativos=True)
        
        for acolhido in all_acolhidos:
            admissao_ativa = db.query(Acolhimento)\
                              .filter(Acolhimento.id_acolhido == acolhido.id_acolhido)\
                              .filter(Acolhimento.status_ativo == True)\
                              .first()
            
            if not admissao_ativa:
                acolhidos_disponiveis.append(acolhido)
        
        abrigos = crud.listar_abrigos(db, ativos=True)
        
        return templates.TemplateResponse("nova_admissao.html", {
            "request": request,
            "acolhidos": acolhidos_disponiveis,
            "abrigos": abrigos,
            "data_hoje": date.today().isoformat()
        })
        
    except Exception as e:
        return templates.TemplateResponse("erro.html", {
            "request": request,
            "erro": f"Erro ao carregar formulário: {str(e)}"
        })


@app.post("/admissoes/criar")
async def criar_admissao_form(
    request: Request,
    acolhido_id: int = Form(...),
    abrigo_id: int = Form(...),
    data_admissao: str = Form(...),
    numero_vaga: str = Form(""),
    db: Session = Depends(get_db)
):
    try:
        admissao_data = schemas.AdmissaoCreate(
            pessoa_id=acolhido_id,
            abrigo_id=abrigo_id,
            data_admissao=date.fromisoformat(data_admissao),
            numero_vaga=numero_vaga if numero_vaga else None
        )
        crud.registrar_admissao(db, admissao_data)
        return RedirectResponse(url="/admissoes", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("erro.html", {
            "request": request,
            "erro": f"Erro ao criar admissão: {str(e)}"
        })


@app.get("/pessoas/nova", response_class=HTMLResponse)
async def nova_pessoa_form(request: Request):
    return templates.TemplateResponse("nova_pessoa.html", {
        "request": request
    })


@app.post("/pessoas/criar")
async def criar_pessoa_form(
    request: Request,
    nome: str = Form(...),
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    telefone: str = Form(...),
    endereco_rua: str = Form(...),
    endereco_bairro: str = Form(...),
    endereco_cidade: str = Form(...),
    endereco_estado: str = Form(...),
    numero_prontuario: str = Form(...),
    motivo_acolhimento: str = Form(...),
    historico_saude: str = Form(""),
    genero: str = Form(""),
    necessidade_especial: str = Form("false"),
    db: Session = Depends(get_db)
):
    try:
        pessoa_data = schemas.PessoaAcolhidaCreate(
            nome=nome,
            cpf=cpf,
            data_nascimento=date.fromisoformat(data_nascimento),
            historico_saude=historico_saude if historico_saude else None,
            genero=genero,
            necessidade_especial=necessidade_especial.lower() == "true",
            telefone_principal=telefone,
            endereco_rua=endereco_rua,
            endereco_bairro=endereco_bairro,
            endereco_cidade=endereco_cidade,
            endereco_estado=endereco_estado,
            motivo_acolhimento=motivo_acolhimento,
            numero_prontuario=numero_prontuario
        )
        crud.criar_pessoa_acolhida(db, pessoa_data)
        return RedirectResponse(url="/admissoes/nova", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("erro.html", {
            "request": request,
            "erro": f"Erro ao criar pessoa: {str(e)}"
        })