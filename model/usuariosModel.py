from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from config.databaseConfig import Base, engine

class Usuarios(Base):
    """
    Modelo da tabela usuarios no banco de dados.
    """
    __tablename__ = "usuarios"
    
    # Campos da tabela
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha = Column(String(100), nullable=False)
    
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
    
    def __repr__(self):
        return f"<Usuario(id={self.id}, nome='{self.nome}', email='{self.email}')>"
    
    def to_dict(self):
        """
        Converte o objeto Usuario em dicionário para serialização JSON.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email
        }