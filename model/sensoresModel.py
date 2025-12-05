from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.databaseConfig import Base, engine

class Sensor(Base):
    """
    Modelo da tabela sensores no banco de dados.
    """
    __tablename__ = "sensores"
    
    # Campos da tabela
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False, index=True)
    tipo = Column(String(50), nullable=False)  # ex: "temperatura", "umidade", "pressao"
    unidade = Column(String(20), nullable=False)  # ex: "°C", "%", "hPa"
    
    # Relacionamento com valores
    valores = relationship("ValoresSensor", back_populates="sensor", cascade="all, delete-orphan")
    
    def __init__(self, nome, tipo, unidade):
        self.nome = nome
        self.tipo = tipo
        self.unidade = unidade
    
    def __repr__(self):
        return f"<Sensor(id={self.id}, nome='{self.nome}', tipo='{self.tipo}', unidade='{self.unidade}')>"
    
    def to_dict(self):
        """
        Converte o objeto Sensor em dicionário para serialização JSON.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": self.tipo,
            "unidade": self.unidade
        }


class ValoresSensor(Base):
    """
    Modelo da tabela valores_sensor no banco de dados.
    """
    __tablename__ = "valores_sensor"
    
    # Campos da tabela
    id_valor = Column(Integer, primary_key=True, index=True, autoincrement=True)
    valor = Column(Float, nullable=False)
    id_sensor = Column(Integer, ForeignKey('sensores.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=func.now())
    
    # Relacionamento com sensor
    sensor = relationship("Sensor", back_populates="valores")
    
    def __init__(self, valor, id_sensor):
        self.valor = valor
        self.id_sensor = id_sensor
    
    def __repr__(self):
        return f"<ValoresSensor(id={self.id_valor}, valor={self.valor}, id_sensor={self.id_sensor}, timestamp={self.timestamp})>"
    
    def to_dict(self):
        """
        Converte o objeto ValoresSensor em dicionário para serialização JSON.
        """
        return {
            "id_valor": self.id_valor,
            "valor": self.valor,
            "id_sensor": self.id_sensor,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }

def criar_tabelas_sensores():
    """
    Função específica para criar as tabelas de sensores e valores.
    """
    try:
        # Criar tabelas de sensores e valores
        Sensor.__table__.create(bind=engine, checkfirst=True)
        ValoresSensor.__table__.create(bind=engine, checkfirst=True)
        print("Tabelas 'sensores' e 'valores_sensor' criadas com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao criar tabelas de sensores: {str(e)}")
        return False

