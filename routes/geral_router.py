from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.databaseConfig import get_database

# Criar router para rotas gerais
router = APIRouter(
    prefix="/api",
    tags=["geral"]
)

@router.get("/")
async def root():
    """Rota principal da API"""
    return {"message": "API de Sensores e Usuários - Funcionando!"}

@router.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {"status": "healthy", "message": "API funcionando corretamente"}

@router.get("/stats")
async def estatisticas_gerais(db: Session = Depends(get_database)):
    """Estatísticas gerais da aplicação"""
    try:
        from service.SensoresService import SensoresService
        from service.UsuariosService import UsuariosService
        
        sensor_service = SensoresService(db)
        usuario_service = UsuariosService(db)
        
        return {
            "total_sensores": sensor_service.contar_total(),
            "total_usuarios": usuario_service.contar_total(),
            "status": "online"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/info")
async def info_api():
    """Informações sobre a API"""
    return {
        "nome": "API de Sensores e Usuários",
        "versao": "1.0.0",
        "descricao": "API REST para gerenciamento de sensores IoT e usuários",
        "endpoints": {
            "sensores": "/sensores",
            "usuarios": "/usuarios", 
            "documentacao": "/docs",
            "saude": "/api/health",
            "estatisticas": "/api/stats"
        }
    }