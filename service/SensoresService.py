from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from model.sensoresModel import Sensor
from typing import List, Optional

class SensoresService:
    """
    Service para operações CRUD de Sensores
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def listar_todos(self) -> List[Sensor]:
        """
        Lista todos os sensores
        """
        try:
            return self.db.query(Sensor).all()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao listar sensores: {str(e)}")
    
    def buscar_por_id(self, sensor_id: int) -> Optional[Sensor]:
        """
        Busca um sensor por ID
        """
        try:
            return self.db.query(Sensor).filter(Sensor.id == sensor_id).first()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar sensor: {str(e)}")
    
    def buscar_por_tipo(self, tipo: str) -> List[Sensor]:
        """
        Busca sensores por tipo
        """
        try:
            return self.db.query(Sensor).filter(Sensor.tipo == tipo).all()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar sensores por tipo: {str(e)}")
    
    def criar(self, nome: str, tipo: str, valor: float, unidade: str) -> Sensor:
        """
        Cria um novo sensor
        """
        try:
            novo_sensor = Sensor(
                nome=nome,
                tipo=tipo,
                valor=valor,
                unidade=unidade
            )
            
            self.db.add(novo_sensor)
            self.db.commit()
            self.db.refresh(novo_sensor)
            
            return novo_sensor
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao criar sensor: {str(e)}")
    
    def atualizar(self, sensor_id: int, nome: Optional[str] = None, 
                  tipo: Optional[str] = None, valor: Optional[float] = None, 
                  unidade: Optional[str] = None) -> Optional[Sensor]:
        """
        Atualiza um sensor existente
        """
        try:
            sensor = self.db.query(Sensor).filter(Sensor.id == sensor_id).first()
            
            if not sensor:
                return None
            
            # Atualizar apenas campos fornecidos
            if nome is not None:
                sensor.nome = nome
            if tipo is not None:
                sensor.tipo = tipo
            if valor is not None:
                sensor.valor = valor
            if unidade is not None:
                sensor.unidade = unidade
            
            self.db.commit()
            self.db.refresh(sensor)
            
            return sensor
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao atualizar sensor: {str(e)}")
    
    def deletar(self, sensor_id: int) -> bool:
        """
        Deleta um sensor
        """
        try:
            sensor = self.db.query(Sensor).filter(Sensor.id == sensor_id).first()
            
            if not sensor:
                return False
            
            self.db.delete(sensor)
            self.db.commit()
            
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao deletar sensor: {str(e)}")
    
    def contar_total(self) -> int:
        """
        Conta total de sensores
        """
        try:
            return self.db.query(Sensor).count()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao contar sensores: {str(e)}")
    
    def buscar_por_nome(self, nome: str) -> List[Sensor]:
        """
        Busca sensores por nome (busca parcial)
        """
        try:
            return self.db.query(Sensor).filter(Sensor.nome.contains(nome)).all()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar sensores por nome: {str(e)}")
