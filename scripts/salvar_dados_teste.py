import sys
import os
from sqlalchemy.orm import Session
from config.databaseConfig import SessionLocal
from model.sensoresModel import Sensor

# Script para inserir dados de temperatura e umidade no banco SQLite

def salvar_dados_temperatura_umidade(temperatura, umidade):
    db: Session = SessionLocal()
    try:
        sensor_temp = Sensor(
            nome="temeratura",
            tipo="temperatura",
            valor=temperatura,
            unidade="°C"
        )
        sensor_umid = Sensor(
            nome="umidade",
            tipo="umidade",
            valor=umidade,
            unidade="%"
        )
        db.add(sensor_temp)
        db.add(sensor_umid)
        db.commit()
        print(f"Dados salvos: Temperatura={temperatura}°C, Umidade={umidade}%")
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Valores fixos para teste
    temperatura = 70
    umidade = 8
    salvar_dados_temperatura_umidade(temperatura, umidade)
