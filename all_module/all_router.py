from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from config.databaseConfig import get_database
from all_module.AllController import AllController

# Criar router para dados JSON (tabela all)
router = APIRouter(
    prefix="/data",
    tags=["dados-json"],
    responses={404: {"description": "Registro não encontrado"}}
)

@router.get("/")
async def listar_dados(
    limite: int = Query(100, description="Número máximo de registros"),
    offset: int = Query(0, description="Número de registros para pular"),
    db: Session = Depends(get_database)
):
    """Lista todos os dados JSON recebidos via MQTT"""
    return await AllController.listar_todos(limite, offset, db)

@router.get("/{record_id}")
async def obter_dado(record_id: int, db: Session = Depends(get_database)):
    """Obtém um registro específico por ID"""
    return await AllController.obter_por_id(record_id, db)

@router.get("/topic/{topic}")
async def listar_por_topico(topic: str, db: Session = Depends(get_database)):
    """Lista registros por tópico MQTT"""
    return await AllController.listar_por_topico(topic, db)

@router.post("/")
async def criar_dado(
    topic: str,
    payload: str,
    db: Session = Depends(get_database)
):
    """Cria um novo registro JSON manualmente"""
    return await AllController.criar_registro(topic, payload, db)

@router.delete("/{record_id}")
async def deletar_dado(record_id: int, db: Session = Depends(get_database)):
    """Deleta um registro"""
    return await AllController.deletar_registro(record_id, db)

@router.get("/search/{search_term}")
async def buscar_no_payload(search_term: str, db: Session = Depends(get_database)):
    """Busca registros que contenham um termo no payload"""
    return await AllController.buscar_no_payload(search_term, db)

@router.get("/topics/list")
async def listar_topicos(db: Session = Depends(get_database)):
    """Lista todos os tópicos únicos"""
    return await AllController.listar_topicos(db)

@router.get("/stats/estatisticas")
async def estatisticas_dados(db: Session = Depends(get_database)):
    """Estatísticas dos dados JSON"""
    return await AllController.estatisticas(db)

@router.delete("/cleanup/{dias}")
async def limpar_dados_antigos(dias: int, db: Session = Depends(get_database)):
    """Remove registros mais antigos que X dias"""
    return await AllController.limpar_antigos(dias, db)