from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from all_module.allModel import All
from typing import List, Optional
import json

class AllService:
    """
    Service para operações CRUD da tabela All (dados JSON)
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def listar_todos(self) -> List[All]:
        """
        Lista todos os registros
        """
        try:
            return self.db.query(All).order_by(All.data_recebimento.desc()).all()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao listar registros: {str(e)}")
    
    def buscar_por_id(self, record_id: int) -> Optional[All]:
        """
        Busca um registro por ID
        """
        try:
            return self.db.query(All).filter(All.id == record_id).first()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar registro: {str(e)}")
    
    def buscar_por_topico(self, topic: str) -> List[All]:
        """
        Busca registros por tópico
        """
        try:
            return self.db.query(All).filter(All.topic == topic).order_by(All.data_recebimento.desc()).all()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar registros por tópico: {str(e)}")
    
    def criar(self, topic: str, payload: str) -> All:
        """
        Cria um novo registro
        """
        try:
            novo_registro = All(topic=topic, payload=payload)
            
            self.db.add(novo_registro)
            self.db.commit()
            self.db.refresh(novo_registro)
            
            return novo_registro
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao criar registro: {str(e)}")
    
    def deletar(self, record_id: int) -> bool:
        """
        Deleta um registro
        """
        try:
            registro = self.db.query(All).filter(All.id == record_id).first()
            
            if not registro:
                return False
            
            self.db.delete(registro)
            self.db.commit()
            
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao deletar registro: {str(e)}")
    
    def contar_total(self) -> int:
        """
        Conta total de registros
        """
        try:
            return self.db.query(All).count()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao contar registros: {str(e)}")
    
    def buscar_por_payload(self, search_term: str) -> List[All]:
        """
        Busca registros que contenham um termo no payload
        """
        try:
            return self.db.query(All).filter(All.payload.contains(search_term)).order_by(All.data_recebimento.desc()).all()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar registros por payload: {str(e)}")
    
    def listar_topicos_unicos(self) -> List[str]:
        """
        Lista todos os tópicos únicos
        """
        try:
            result = self.db.query(All.topic).distinct().all()
            return [row[0] for row in result]
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao listar tópicos únicos: {str(e)}")
    
    def listar_com_limite(self, limite: int = 100, offset: int = 0) -> List[All]:
        """
        Lista registros com paginação
        """
        try:
            return self.db.query(All).order_by(All.data_recebimento.desc()).offset(offset).limit(limite).all()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao listar registros com limite: {str(e)}")
    
    def limpar_registros_antigos(self, dias: int = 30) -> int:
        """
        Remove registros mais antigos que X dias
        """
        try:
            from datetime import datetime, timedelta
            data_limite = datetime.now() - timedelta(days=dias)
            
            registros_antigos = self.db.query(All).filter(All.data_recebimento < data_limite)
            count = registros_antigos.count()
            registros_antigos.delete()
            
            self.db.commit()
            return count
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao limpar registros antigos: {str(e)}")