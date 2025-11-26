from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from config.databaseConfig import Base, engine

class Alerta(Base):
    """
    Modelo da tabela alerta no banco de dados.
    """
    __tablename__ = "alerta"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False, index=True)
    data = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f"<Alerta(id={self.id}, nome='{self.nome}', data='{self.data}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data": self.data.isoformat() if self.data else None
        }

def criar_tabela_alerta():
    try:
        Alerta.__table__.create(bind=engine, checkfirst=True)
        print("Tabela 'alerta' criada com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao criar tabela 'alerta': {str(e)}")
        return False
