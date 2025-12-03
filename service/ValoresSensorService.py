from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from model.sensoresModel import ValoresSensor, Sensor
from typing import List, Optional

class ValoresSensorService:
    """
    Service para operações CRUD de Valores dos Sensores
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def criar_valor(self, valor: float, id_sensor: int) -> ValoresSensor:
        """
        Cria um novo valor para um sensor
        """
        try:
            # Verificar se o sensor existe
            sensor = self.db.query(Sensor).filter(Sensor.id == id_sensor).first()
            if not sensor:
                raise Exception(f"Sensor com ID {id_sensor} não encontrado")
            
            novo_valor = ValoresSensor(
                valor=valor,
                id_sensor=id_sensor
            )
            
            self.db.add(novo_valor)
            self.db.commit()
            self.db.refresh(novo_valor)
            
            return novo_valor
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao criar valor do sensor: {str(e)}")
    
    def listar_valores_por_sensor(self, id_sensor: int, limit: int = 100) -> List[ValoresSensor]:
        """
        Lista os valores de um sensor específico (mais recentes primeiro)
        """
        try:
            return self.db.query(ValoresSensor).filter(
                ValoresSensor.id_sensor == id_sensor
            ).order_by(desc(ValoresSensor.timestamp)).limit(limit).all()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao listar valores do sensor: {str(e)}")
    
    def obter_ultimo_valor(self, id_sensor: int) -> Optional[ValoresSensor]:
        """
        Obtém o último valor registrado de um sensor
        """
        try:
            return self.db.query(ValoresSensor).filter(
                ValoresSensor.id_sensor == id_sensor
            ).order_by(desc(ValoresSensor.timestamp)).first()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao obter último valor do sensor: {str(e)}")
    
    def obter_valor_por_id(self, id_valor: int) -> Optional[ValoresSensor]:
        """
        Busca um valor por ID
        """
        try:
            return self.db.query(ValoresSensor).filter(ValoresSensor.id_valor == id_valor).first()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar valor: {str(e)}")
    
    def deletar_valor(self, id_valor: int) -> bool:
        """
        Deleta um valor
        """
        try:
            valor = self.db.query(ValoresSensor).filter(ValoresSensor.id_valor == id_valor).first()
            
            if not valor:
                return False
            
            self.db.delete(valor)
            self.db.commit()
            
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao deletar valor: {str(e)}")
    
    def contar_valores_por_sensor(self, id_sensor: int) -> int:
        """
        Conta total de valores de um sensor
        """
        try:
            return self.db.query(ValoresSensor).filter(ValoresSensor.id_sensor == id_sensor).count()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao contar valores do sensor: {str(e)}")
    
    def listar_todos_valores(self, limit: int = 1000) -> List[ValoresSensor]:
        """
        Lista todos os valores (mais recentes primeiro)
        """
        try:
            return self.db.query(ValoresSensor).order_by(desc(ValoresSensor.timestamp)).limit(limit).all()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao listar valores: {str(e)}")
    
    def deletar_valores_antigos(self, id_sensor: int, manter_ultimos: int = 1000) -> int:
        """
        Deleta valores antigos de um sensor, mantendo apenas os N mais recentes
        """
        try:
            # Buscar IDs dos valores mais recentes que devem ser mantidos
            valores_manter = self.db.query(ValoresSensor.id_valor).filter(
                ValoresSensor.id_sensor == id_sensor
            ).order_by(desc(ValoresSensor.timestamp)).limit(manter_ultimos).subquery()
            
            # Deletar valores que não estão na lista dos que devem ser mantidos
            deletados = self.db.query(ValoresSensor).filter(
                ValoresSensor.id_sensor == id_sensor,
                ValoresSensor.id_valor.notin_(valores_manter)
            ).delete(synchronize_session=False)
            
            self.db.commit()
            
            return deletados
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao deletar valores antigos: {str(e)}")