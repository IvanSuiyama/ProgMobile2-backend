from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

 # Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///./estacao_esp32.db"

# Criar o engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necessário para SQLite
)

# Criar SessionLocal para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Metadados para operações de esquema
metadata = MetaData()

def get_database():
    """
    Função generator para obter uma sessão do banco de dados.
    Usado como dependency no FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Função para criar todas as tabelas no banco de dados.
    """
    # Importar todos os modelos para garantir que sejam registrados
    from model.sensoresModel import Sensor, ValoresSensor
    from model.usuariosModel import Usuarios
    from all_module.allModel import All
    from model.alertaModel import Alerta
    
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")
    print("- Tabela 'sensores' criada")
    print("- Tabela 'valores_sensor' criada")
    print("- Tabela 'usuarios' criada")
    print("- Tabela 'all' criada")
    print("- Tabela 'alerta' criada")

def get_database_path():
    """
    Retorna o caminho do arquivo do banco de dados.
    """
    return "./estacao_esp32.db"

def database_exists():
    """
    Verifica se o arquivo do banco de dados existe.
    """
    return os.path.exists(get_database_path())
