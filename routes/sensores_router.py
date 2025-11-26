from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.databaseConfig import get_database
from controller.SensoresController import SensoresController

# Criar router para sensores
router = APIRouter(
    prefix="/sensores",
    tags=["sensores"],
    responses={404: {"description": "Sensor não encontrado"}}
)

@router.get("/")
async def listar_sensores(db: Session = Depends(get_database)):
    """Lista todos os sensores"""
    return await SensoresController.listar_sensores(db)

@router.get("/{sensor_id}")
async def obter_sensor(sensor_id: int, db: Session = Depends(get_database)):
    """Obtém um sensor específico"""
    return await SensoresController.obter_sensor(sensor_id, db)

@router.get("/tipo/{tipo_sensor}")
async def listar_sensores_por_tipo(tipo_sensor: str, db: Session = Depends(get_database)):
    """Lista sensores por tipo"""
    return await SensoresController.listar_sensores_por_tipo(tipo_sensor, db)

@router.post("/")
async def criar_sensor(
    nome: str,
    tipo: str, 
    valor: float,
    unidade: str,
    db: Session = Depends(get_database)
):
    """Cria um novo sensor"""
    return await SensoresController.criar_sensor(nome, tipo, valor, unidade, db)

@router.put("/{sensor_id}")
async def atualizar_sensor(
    sensor_id: int,
    nome: str = None,
    tipo: str = None,
    valor: float = None,
    unidade: str = None,
    db: Session = Depends(get_database)
):
    """Atualiza um sensor"""
    return await SensoresController.atualizar_sensor(sensor_id, nome, tipo, valor, unidade, db)

@router.delete("/{sensor_id}")
async def deletar_sensor(sensor_id: int, db: Session = Depends(get_database)):
    """Deleta um sensor"""
    return await SensoresController.deletar_sensor(sensor_id, db)

@router.get("/buscar/{nome}")
async def buscar_sensores_por_nome(nome: str, db: Session = Depends(get_database)):
    """Busca sensores por nome"""
    return await SensoresController.buscar_sensores_por_nome(nome, db)

@router.get("/stats/estatisticas")
async def estatisticas_sensores(db: Session = Depends(get_database)):
    """Estatísticas dos sensores"""
    return await SensoresController.estatisticas_sensores(db)