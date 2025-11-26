import os
import sys
from pathlib import Path

# Garantir que o root do projeto esteja no sys.path quando o script for
# executado diretamente (ex.: python3 scripts/reset_db.py).
# Isso evita o erro ModuleNotFoundError: No module named 'config'
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.databaseConfig import Base, engine, get_database_path
from model.sensoresModel import Sensor
from model.usuariosModel import Usuarios
from all_module.allModel import All
from model.alertaModel import Alerta


def main():
    print("🔄 Recriando banco de dados...")
    
    # 1. Deletar o arquivo do banco se existir
    db_file = get_database_path()
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"✅ Banco '{db_file}' deletado!")
    
    # 2. Criar todas as tabelas
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas!")
    
    # 3. Verificar quais tabelas foram criadas
    from config.databaseConfig import SessionLocal
    from sqlalchemy import text
    db = SessionLocal()
    try:
        # Verificar se as tabelas existem
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tabelas = [row[0] for row in result.fetchall()]
        print(f"📊 Tabelas encontradas no banco: {', '.join(tabelas)}")
        print("📋 Tabelas esperadas: sensores, usuarios, all, alerta")
    except Exception as e:
        print(f"⚠️ Erro ao verificar tabelas: {e}")
    finally:
        db.close()
    
    print("🎉 Pronto! Banco recriado com sucesso!")

if __name__ == "__main__":
    main()