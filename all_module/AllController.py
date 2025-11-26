from fastapi import HTTPException, Depends, Query
from sqlalchemy.orm import Session
from config.databaseConfig import get_database
from all_module.AllService import AllService
from typing import List, Optional

class AllController:
    """
    Controller para endpoints da tabela All (dados JSON)
    """
    
    @staticmethod
    async def listar_todos(
        limite: int = Query(100, description="Número máximo de registros"),
        offset: int = Query(0, description="Número de registros para pular"),
        db: Session = Depends(get_database)
    ) -> List[dict]:
        """
        Lista todos os registros JSON com paginação
        """
        try:
            service = AllService(db)
            registros = service.listar_com_limite(limite, offset)
            return [registro.to_dict() for registro in registros]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def obter_por_id(record_id: int, db: Session = Depends(get_database)) -> dict:
        """
        Obtém um registro específico por ID
        """
        try:
            service = AllService(db)
            registro = service.buscar_por_id(record_id)
            
            if registro is None:
                raise HTTPException(status_code=404, detail="Registro não encontrado")
            
            return registro.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def listar_por_topico(topic: str, db: Session = Depends(get_database)) -> List[dict]:
        """
        Lista registros por tópico MQTT
        """
        try:
            service = AllService(db)
            registros = service.buscar_por_topico(topic)
            return [registro.to_dict() for registro in registros]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def criar_registro(
        topic: str,
        payload: str,
        db: Session = Depends(get_database)
    ) -> dict:
        """
        Cria um novo registro JSON manualmente
        """
        try:
            # Validações básicas
            if not topic or not payload:
                raise HTTPException(status_code=400, detail="Tópico e payload são obrigatórios")
            
            service = AllService(db)
            novo_registro = service.criar(topic, payload)
            
            return novo_registro.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def deletar_registro(record_id: int, db: Session = Depends(get_database)) -> dict:
        """
        Deleta um registro
        """
        try:
            service = AllService(db)
            sucesso = service.deletar(record_id)
            
            if not sucesso:
                raise HTTPException(status_code=404, detail="Registro não encontrado")
            
            return {"message": f"Registro {record_id} deletado com sucesso"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def buscar_no_payload(search_term: str, db: Session = Depends(get_database)) -> List[dict]:
        """
        Busca registros que contenham um termo no payload
        """
        try:
            if not search_term:
                raise HTTPException(status_code=400, detail="Termo de busca é obrigatório")
            
            service = AllService(db)
            registros = service.buscar_por_payload(search_term)
            return [registro.to_dict() for registro in registros]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def listar_topicos(db: Session = Depends(get_database)) -> List[str]:
        """
        Lista todos os tópicos únicos
        """
        try:
            service = AllService(db)
            return service.listar_topicos_unicos()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def estatisticas(db: Session = Depends(get_database)) -> dict:
        """
        Retorna estatísticas dos dados JSON
        """
        try:
            service = AllService(db)
            total = service.contar_total()
            topicos = service.listar_topicos_unicos()
            
            return {
                "total_registros": total,
                "total_topicos": len(topicos),
                "topicos": topicos
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def limpar_antigos(dias: int = 30, db: Session = Depends(get_database)) -> dict:
        """
        Remove registros mais antigos que X dias
        """
        try:
            if dias < 1:
                raise HTTPException(status_code=400, detail="Número de dias deve ser maior que 0")
            
            service = AllService(db)
            removidos = service.limpar_registros_antigos(dias)
            
            return {
                "message": f"Limpeza concluída",
                "registros_removidos": removidos,
                "dias": dias
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))