#!/usr/bin/env python3
"""
Script para inserir dados de teste de temperatura e umidade usando a nova arquitetura
Cria sensores (se não existirem) e valores na tabela valores_sensor
"""

import sys
import os
from sqlalchemy.orm import Session
from config.databaseConfig import SessionLocal
from service.SensoresService import SensoresService
from service.ValoresSensorService import ValoresSensorService

def salvar_dados_temperatura_umidade(temperatura, umidade):
    """
    Salva dados de teste de temperatura e umidade usando a nova arquitetura
    """
    db: Session = SessionLocal()
    try:
        sensores_service = SensoresService(db)
        valores_service = ValoresSensorService(db)
        
        # Buscar ou criar sensor de temperatura
        sensor_temp = buscar_ou_criar_sensor(
            sensores_service, 
            nome="temperatura_teste",
            tipo="temperatura", 
            unidade="°C"
        )
        
        # Buscar ou criar sensor de umidade  
        sensor_umid = buscar_ou_criar_sensor(
            sensores_service,
            nome="umidade_teste", 
            tipo="umidade",
            unidade="%"
        )
        
        if sensor_temp and sensor_umid:
            # Criar valores para os sensores
            valor_temp = valores_service.criar_valor(valor=temperatura, id_sensor=sensor_temp.id)
            valor_umid = valores_service.criar_valor(valor=umidade, id_sensor=sensor_umid.id)
            
            if valor_temp and valor_umid:
                print(f"✅ Dados de teste salvos com sucesso!")
                print(f"🌡️ Temperatura: {temperatura}°C (Sensor ID: {sensor_temp.id})")
                print(f"💧 Umidade: {umidade}% (Sensor ID: {sensor_umid.id})")
            else:
                print("❌ Erro ao criar valores para os sensores")
        else:
            print("❌ Erro ao buscar/criar sensores")
            
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")
        db.rollback()
    finally:
        db.close()

def buscar_ou_criar_sensor(sensores_service, nome, tipo, unidade):
    """
    Busca um sensor por nome ou cria se não existir
    """
    try:
        # Buscar sensor existente
        sensores = sensores_service.listar_todos()
        for sensor in sensores:
            if sensor.nome.lower() == nome.lower():
                print(f"🔍 Sensor '{nome}' já existe (ID: {sensor.id})")
                return sensor
        
        # Criar novo sensor se não existir
        novo_sensor = sensores_service.criar(nome=nome, tipo=tipo, unidade=unidade)
        print(f"🆕 Sensor '{nome}' criado com sucesso (ID: {novo_sensor.id})")
        return novo_sensor
        
    except Exception as e:
        print(f"❌ Erro ao buscar/criar sensor '{nome}': {e}")
        return None

if __name__ == "__main__":
    print("🧪 === SCRIPT DE DADOS DE TESTE ===")
    print("Este script cria sensores de teste e insere valores usando a nova arquitetura")
    print()
    
    # Valores de teste (críticos para ativar alertas)
    temperatura = 75.5  # Acima do limite de 70°C
    umidade = 5.0       # Abaixo do limite de 10%
    
    salvar_dados_temperatura_umidade(temperatura, umidade)
    
    print("\n🏁 Script finalizado!")
    print("💡 Dica: Verifique os alertas no frontend ou rode o monitoramento de alertas")
