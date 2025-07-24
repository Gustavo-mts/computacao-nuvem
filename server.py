"""
Sistema de Gestão para Abrigos
Servidor Web - FastAPI Application Server

Este módulo inicializa e executa o servidor web para o sistema de gestão
de abrigos, fornecendo interface web em desenvolvimento para gerenciamento.
"""

import uvicorn
from app.api import app


def main():
    
    print("Iniciando Sistema de Gestão para Abrigos...")
    print("Servidor web sendo inicializado...")
    print("")
    print("URLs do Sistema:")
    print("  Aplicação Principal: http://localhost:8000")
    print("  Dashboard:          http://localhost:8000/")
    print("  Gestão de Abrigos:  http://localhost:8000/abrigos")
    print("  Funcionários:       http://localhost:8000/funcionarios")
    print("  Admissões:          http://localhost:8000/admissoes")
    print("")
    print("Para parar o servidor: Ctrl+C")
    print("="*60)
    
    # Configurações do servidor
    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",              #conexões de qualquer IP
        port=8000,                   #padrão HTTP alternativa
        reload=True,                 # Auto-reload 
        reload_dirs=["app", "templates"],#Diretórios monitorados
        log_level="info",            
        access_log=True             
    )


if __name__ == "__main__":
    main()