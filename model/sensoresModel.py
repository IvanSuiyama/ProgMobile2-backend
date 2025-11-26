from sqlalchemy import Column, Integer, String, Float, Boolean
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
    valor = Column(Float, nullable=False)
    unidade = Column(String(20), nullable=False)  # ex: "°C", "%", "hPa"
    
    def __init__(self, nome, tipo, valor, unidade):
        self.nome = nome
        self.tipo = tipo
        self.valor = valor
        self.unidade = unidade
    
    def __repr__(self):
        return f"<Sensor(id={self.id}, nome='{self.nome}', tipo='{self.tipo}', valor={self.valor})>"
    
    def to_dict(self):
        """
        Converte o objeto Sensor em dicionário para serialização JSON.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": self.tipo,
            "valor": self.valor,
            "unidade": self.unidade
        }

def criar_tabela_sensores():
    """
    Função específica para criar a tabela de sensores.
    """
    try:
        # Criar apenas a tabela de sensores
        Sensor.__table__.create(bind=engine, checkfirst=True)
        print("Tabela 'sensores' criada com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao criar tabela 'sensores': {str(e)}")
        return False

