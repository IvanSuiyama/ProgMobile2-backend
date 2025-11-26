from sqlalchemy import Column, Integer, Text
from config.databaseConfig import Base, engine
import json

class All(Base):
    """
    Modelo da tabela all no banco de dados.
    Armazena dados JSON puros recebidos via MQTT.
    """
    __tablename__ = "all"
    
    # Campos da tabela
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    topic = Column(Text, nullable=False, index=True)  # Tópico MQTT de origem
    payload = Column(Text, nullable=False)  # JSON como string
    
    def __init__(self, topic: str, payload: str):
        self.topic = topic
        self.payload = payload
    
    def __repr__(self):
        return f"<All(id={self.id}, topic='{self.topic}')>"
    
    def to_dict(self):
        """
        Converte o objeto All em dicionário para serialização JSON.
        """
        try:
            # Tentar parsear o payload como JSON
            payload_json = json.loads(self.payload)
        except json.JSONDecodeError:
            # Se não for JSON válido, manter como string
            payload_json = self.payload
            
        return {
            "id": self.id,
            "topic": self.topic,
            "payload": payload_json
        }
    
    def get_payload_json(self):
        """
        Retorna o payload como objeto JSON.
        """
        try:
            return json.loads(self.payload)
        except json.JSONDecodeError:
            return None

def criar_tabela_all():
    """
    Função específica para criar a tabela all.
    """
    try:
        # Criar apenas a tabela all
        All.__table__.create(bind=engine, checkfirst=True)
        print("Tabela 'all' criada com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao criar tabela 'all': {str(e)}")
        return False