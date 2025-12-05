from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from config.databaseConfig import get_database
from service.SensoresService import SensoresService
from typing import List, Optional

class SensoresController:
    """
    Controller para endpoints de Sensores
    """
    
    @staticmethod
    async def listar_sensores(db: Session = Depends(get_database)) -> List[dict]:
        """
        Lista todos os sensores
        """
        try:
            service = SensoresService(db)
            sensores = service.listar_todos()
            return [sensor.to_dict() for sensor in sensores]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def obter_sensor(sensor_id: int, db: Session = Depends(get_database)) -> dict:
        """
        Obtém um sensor específico por ID
        """
        try:
            service = SensoresService(db)
            sensor = service.buscar_por_id(sensor_id)
            
            if sensor is None:
                raise HTTPException(status_code=404, detail="Sensor não encontrado")
            
            return sensor.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def listar_sensores_por_tipo(tipo_sensor: str, db: Session = Depends(get_database)) -> List[dict]:
        """
        Lista sensores por tipo
        """
        try:
            service = SensoresService(db)
            sensores = service.buscar_por_tipo(tipo_sensor)
            return [sensor.to_dict() for sensor in sensores]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def criar_sensor(
        nome: str,
        tipo: str,
        unidade: str,
        db: Session = Depends(get_database)
    ) -> dict:
        """
        Cria um novo sensor
        """
        try:
            # Validações básicas
            if not nome or not tipo or not unidade:
                raise HTTPException(status_code=400, detail="Nome, tipo e unidade são obrigatórios")
            
            service = SensoresService(db)
            novo_sensor = service.criar(nome, tipo, unidade)
            
            return novo_sensor.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def atualizar_sensor(
        sensor_id: int,
        nome: Optional[str] = None,
        tipo: Optional[str] = None,
        unidade: Optional[str] = None,
        db: Session = Depends(get_database)
    ) -> dict:
        """
        Atualiza um sensor existente
        """
        try:
            service = SensoresService(db)
            sensor_atualizado = service.atualizar(sensor_id, nome, tipo, unidade)
            
            if sensor_atualizado is None:
                raise HTTPException(status_code=404, detail="Sensor não encontrado")
            
            return sensor_atualizado.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def deletar_sensor(sensor_id: int, db: Session = Depends(get_database)) -> dict:
        """
        Deleta um sensor
        """
        try:
            service = SensoresService(db)
            sucesso = service.deletar(sensor_id)
            
            if not sucesso:
                raise HTTPException(status_code=404, detail="Sensor não encontrado")
            
            return {"message": f"Sensor {sensor_id} deletado com sucesso"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def buscar_sensores_por_nome(nome: str, db: Session = Depends(get_database)) -> List[dict]:
        """
        Busca sensores por nome
        """
        try:
            if not nome:
                raise HTTPException(status_code=400, detail="Nome é obrigatório para busca")
            
            service = SensoresService(db)
            sensores = service.buscar_por_nome(nome)
            return [sensor.to_dict() for sensor in sensores]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def estatisticas_sensores(db: Session = Depends(get_database)) -> dict:
        """
        Retorna estatísticas dos sensores
        """
        try:
            service = SensoresService(db)
            total = service.contar_total()
            
            # Contar por tipo
            sensores = service.listar_todos()
            tipos = {}
            for sensor in sensores:
                if sensor.tipo in tipos:
                    tipos[sensor.tipo] += 1
                else:
                    tipos[sensor.tipo] = 1
            
            return {
                "total_sensores": total,
                "sensores_por_tipo": tipos
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))