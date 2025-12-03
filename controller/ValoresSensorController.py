from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.databaseConfig import get_database
from service.ValoresSensorService import ValoresSensorService

router = APIRouter(prefix="/valores", tags=["Valores dos Sensores"])

@router.post("/{id_sensor}", summary="Criar novo valor para sensor")
async def criar_valor(id_sensor: int, valor: float, db: Session = Depends(get_database)):
    """
    Cria um novo valor para um sensor específico
    """
    try:
        service = ValoresSensorService(db)
        novo_valor = service.criar_valor(valor=valor, id_sensor=id_sensor)
        return novo_valor.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id_sensor}", summary="Listar valores de um sensor")
async def listar_valores_sensor(id_sensor: int, limit: int = 100, db: Session = Depends(get_database)):
    """
    Lista os valores de um sensor específico (mais recentes primeiro)
    """
    try:
        service = ValoresSensorService(db)
        valores = service.listar_valores_por_sensor(id_sensor=id_sensor, limit=limit)
        return [valor.to_dict() for valor in valores]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id_sensor}/ultimo", summary="Obter último valor de um sensor")
async def obter_ultimo_valor(id_sensor: int, db: Session = Depends(get_database)):
    """
    Obtém o último valor registrado de um sensor
    """
    try:
        service = ValoresSensorService(db)
        ultimo_valor = service.obter_ultimo_valor(id_sensor=id_sensor)
        
        if not ultimo_valor:
            return {"valor": None, "timestamp": None}
        
        return ultimo_valor.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", summary="Listar todos os valores")
async def listar_todos_valores(limit: int = 1000, db: Session = Depends(get_database)):
    """
    Lista todos os valores de todos os sensores (mais recentes primeiro)
    """
    try:
        service = ValoresSensorService(db)
        valores = service.listar_todos_valores(limit=limit)
        return [valor.to_dict() for valor in valores]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/valor/{id_valor}", summary="Deletar um valor específico")
async def deletar_valor(id_valor: int, db: Session = Depends(get_database)):
    """
    Deleta um valor específico
    """
    try:
        service = ValoresSensorService(db)
        sucesso = service.deletar_valor(id_valor=id_valor)
        
        if not sucesso:
            raise HTTPException(status_code=404, detail="Valor não encontrado")
        
        return {"detail": "Valor deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id_sensor}/estatisticas", summary="Estatísticas de um sensor")
async def estatisticas_sensor(id_sensor: int, db: Session = Depends(get_database)):
    """
    Obtém estatísticas de um sensor (total de valores, último valor, etc.)
    """
    try:
        service = ValoresSensorService(db)
        
        total_valores = service.contar_valores_por_sensor(id_sensor=id_sensor)
        ultimo_valor = service.obter_ultimo_valor(id_sensor=id_sensor)
        
        return {
            "id_sensor": id_sensor,
            "total_valores": total_valores,
            "ultimo_valor": ultimo_valor.to_dict() if ultimo_valor else None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_sensor}/limpeza", summary="Limpar valores antigos")
async def limpar_valores_antigos(id_sensor: int, manter_ultimos: int = 1000, db: Session = Depends(get_database)):
    """
    Remove valores antigos de um sensor, mantendo apenas os N mais recentes
    """
    try:
        service = ValoresSensorService(db)
        deletados = service.deletar_valores_antigos(id_sensor=id_sensor, manter_ultimos=manter_ultimos)
        
        return {
            "detail": f"{deletados} valores antigos foram removidos",
            "mantidos": manter_ultimos
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))