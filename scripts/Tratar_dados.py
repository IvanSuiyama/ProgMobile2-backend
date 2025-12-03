#!/usr/bin/env python3
"""
Script para processar os dados JSON da tabela 'all' e inserir/atualizar sensores
"""

import json
import asyncio
from datetime import datetime
from all_module.AllService import AllService
from service.SensoresService import SensoresService
from service.ValoresSensorService import ValoresSensorService
from config.databaseConfig import SessionLocal

class TratarDados:
    """
    Classe responsável por processar dados JSON e gerenciar sensores
    """
    
    def __init__(self):
        self.db = SessionLocal()
        self.all_service = AllService(self.db)
        self.sensores_service = SensoresService(self.db)
        self.valores_service = ValoresSensorService(self.db)
    
    def __del__(self):
        """
        Fecha a sessão do banco ao destruir o objeto
        """
        if hasattr(self, 'db'):
            self.db.close()
        
    async def processar_todos_dados(self):
        """
        Processa todos os dados não processados da tabela 'all'
        """
        print("🔄 === INICIANDO PROCESSAMENTO DE DADOS ===")
        
        try:
            # Buscar todos os registros da tabela 'all'
            registros = await self.all_service.get_all_data()
            
            if not registros:
                print("📝 Nenhum dado para processar.")
                return
                
            print(f"📊 Encontrados {len(registros)} registros para processar")
            
            processados = 0
            erros = 0
            
            for registro in registros:
                try:
                    sucesso = await self.processar_registro(registro)
                    if sucesso:
                        processados += 1
                    else:
                        erros += 1
                except Exception as e:
                    print(f"❌ Erro ao processar registro ID {registro.id}: {e}")
                    erros += 1
            
            print(f"\n📈 === RESUMO DO PROCESSAMENTO ===")
            print(f"✅ Processados com sucesso: {processados}")
            print(f"❌ Erros: {erros}")
            print(f"📊 Total: {len(registros)}")
            
        except Exception as e:
            print(f"❌ Erro geral no processamento: {e}")
    
    async def processar_registro(self, registro):
        """
        Processa um registro específico da tabela 'all'
        """
        try:
            print(f"\n🔍 Processando registro ID: {registro.id}")
            print(f"📡 Tópico: {registro.topic}")
            print(f"📦 Payload: {registro.payload}")
            
            # Tentar parsear o JSON
            try:
                dados_json = json.loads(registro.payload)
            except json.JSONDecodeError as e:
                print(f"❌ JSON inválido no registro {registro.id}: {e}")
                return False
                
            # Processar diferentes formatos de dados
            if await self.processar_dados_raspberry(dados_json):
                print(f"✅ Registro {registro.id} processado com sucesso!")
                return True
            else:
                print(f"⚠️ Registro {registro.id} não foi processado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao processar registro {registro.id}: {e}")
            return False
    
    async def processar_dados_raspberry(self, dados_json):
        """
        Processa dados específicos do Raspberry Pi
        """
        try:
            # Verificar se tem a estrutura esperada do Raspberry Pi
            if isinstance(dados_json, dict):
                # Filtrar campos que não são sensores
                campos_ignorar = ['timestamp', 'device_id', 'botao']
                sensores_data = {k: v for k, v in dados_json.items() 
                               if k not in campos_ignorar and v is not None}
                
                if sensores_data:
                    return await self.processar_sensores_dict(sensores_data)
                else:
                    print("⚠️ Nenhum dado de sensor válido encontrado")
                    return False
            
            else:
                print(f"⚠️ Formato de dados não reconhecido: {type(dados_json)}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao processar dados Raspberry Pi: {e}")
            return False
    
    async def processar_sensores_dict(self, sensores_dict):
        """
        Processa um dicionário de sensores {nome: valor}
        """
        sucessos = 0
        
        for nome_sensor, valor in sensores_dict.items():
            try:
                # Pular campos que não são sensores
                if nome_sensor.lower() in ['device_id', 'timestamp', 'location', 'battery']:
                    continue
                    
                print(f"  🔧 Processando sensor: {nome_sensor} = {valor}")
                
                # Verificar se o sensor já existe no banco
                sensor_existente = self.buscar_sensor_por_nome(nome_sensor)
                
                if sensor_existente:
                    # Criar novo valor para o sensor existente
                    if self.criar_valor_sensor_sync(sensor_existente, valor):
                        sucessos += 1
                else:
                    print(f"  ⚠️ Sensor '{nome_sensor}' não encontrado no banco de dados")
                    print(f"  💡 Dica: Crie o sensor '{nome_sensor}' pelo frontend primeiro!")
                    
            except Exception as e:
                print(f"  ❌ Erro ao processar sensor '{nome_sensor}': {e}")
        
        return sucessos > 0
    
    def buscar_sensor_por_nome(self, nome):
        """
        Busca um sensor pelo nome
        """
        try:
            sensores = self.sensores_service.listar_todos()
            for sensor in sensores:
                if sensor.nome.lower() == nome.lower():
                    return sensor
            return None
        except Exception as e:
            print(f"❌ Erro ao buscar sensor por nome '{nome}': {e}")
            return None
    
    async def criar_valor_sensor(self, sensor, novo_valor):
        """
        Cria um novo valor para o sensor
        """
        try:
            # Converter valor para float se possível
            if isinstance(novo_valor, (int, float)):
                valor_float = float(novo_valor)
            elif isinstance(novo_valor, str):
                try:
                    valor_float = float(novo_valor)
                except ValueError:
                    print(f"  ⚠️ Valor '{novo_valor}' não é numérico para sensor '{sensor.nome}'")
                    return False
            else:
                print(f"  ⚠️ Tipo de valor inválido para sensor '{sensor.nome}': {type(novo_valor)}")
                return False
            
            # Criar novo valor para o sensor
            novo_valor_obj = self.valores_service.criar_valor(
                valor=valor_float,
                id_sensor=sensor.id
            )
            
            if novo_valor_obj:
                print(f"  ✅ Valor criado para sensor '{sensor.nome}': {valor_float} {sensor.unidade}")
                return True
            else:
                print(f"  ❌ Falha ao criar valor para sensor '{sensor.nome}'")
                return False
                
        except Exception as e:
            print(f"  ❌ Erro ao criar valor para sensor '{sensor.nome}': {e}")
            return False

async def main():
    """
    Função principal do script
    """
    print("🚀 === SCRIPT DE TRATAMENTO DE DADOS ===")
    print("Este script processa dados JSON da tabela 'all'")
    print("e atualiza sensores existentes no banco de dados.")
    print()
    
    tratador = TratarDados()
    
    try:
        await tratador.processar_todos_dados()
    except KeyboardInterrupt:
        print("\n⏹️ Script interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
    
    print("\n🏁 Script finalizado!")

if __name__ == "__main__":
    # Executar o script
    asyncio.run(main())