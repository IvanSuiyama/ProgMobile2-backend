#!/usr/bin/env python3
"""
Script para simulação de sensores de temperatura e umidade
e publicação dos dados via MQTT
"""

import time
import json
import logging
import random
from datetime import datetime
import paho.mqtt.client as mqtt

# ==============================================================
# CONFIGURAÇÕES
# ==============================================================

# MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "raspberry/sensores"

# GPIO Pinos (equivale ao pinMode() do Arduino)
DHT_PIN = 4          # Sensor DHT11 (Temperatura e Umidade)
LDR_PIN = 24         # Sensor LDR (Luminosidade) - Leitura digital por tempo RC
LED_VERDE_PIN = 21   # LED indicador - funcionamento normal
LED_VERMELHO_PIN = 20 # LED indicador - erro/alerta

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==============================================================
# CLASSE PARA GERENCIAR SENSORES
# ==============================================================

class SensorGPIO:
    """
    Classe para gerenciar sensores conectados ao GPIO do Raspberry Pi
    """
    
    def __init__(self):
        """Inicializa sensores em modo simulação"""
        import math
        self.temperatura_base = 25.0
        self.umidade_base = 60.0
        self.variacao_tempo = 0
        logger.info("✅ Sensores inicializados em modo simulação!")
    
    def ler_temperatura_umidade(self):
        """
        Simula leitura de temperatura e umidade com variações realísticas
        """
        import random
        import math
        
        # Incrementar contador de tempo para variações
        self.variacao_tempo += 1
        
        # Temperatura varia entre 18°C e 35°C com padrão senoidal
        variacao_temp = math.sin(self.variacao_tempo * 0.01) * 5
        temperatura = round(self.temperatura_base + variacao_temp + random.uniform(-2, 2), 1)
        temperatura = max(18.0, min(35.0, temperatura))
        
        # Umidade varia entre 30% e 85% inversamente relacionada à temperatura
        variacao_umidade = math.cos(self.variacao_tempo * 0.01) * 10
        umidade = round(self.umidade_base + variacao_umidade + random.uniform(-5, 5), 1)
        umidade = max(30.0, min(85.0, umidade))
        
        logger.debug(f"🌡️ Simulação - Temp: {temperatura}°C, Umidade: {umidade}%")
        return temperatura, umidade
    
    def ler_luminosidade(self):
        """
        Simula leitura de luminosidade com variação diurna realística
        """
        import random
        import math
        from datetime import datetime
        
        # Simular ciclo dia/noite baseado na hora atual
        hora_atual = datetime.now().hour
        
        if 6 <= hora_atual <= 18:  # Período diurno (6h às 18h)
            # Luminosidade alta durante o dia com pico ao meio-dia
            luz_base = 200 + (600 * math.sin((hora_atual - 6) * math.pi / 12))
        else:  # Período noturno
            luz_base = 50 + random.uniform(-20, 30)
            
        # Adicionar variação aleatória para simular nuvens/sombras
        luminosidade = round(luz_base + random.uniform(-50, 50))
        luminosidade = max(0, min(1023, luminosidade))  # Manter na faixa 0-1023
        
        logger.debug(f"💡 Simulação - Luminosidade: {luminosidade}")
        return luminosidade
    

    
    def controlar_leds(self, verde=False, vermelho=False):
        """
        Simula controle de LEDs (apenas log em modo simulação)
        """
        status = []
        if verde: status.append("VERDE")
        if vermelho: status.append("VERMELHO")
        
        if status:
            logger.debug(f"🚥 LEDs: {', '.join(status)}")
        else:
            logger.debug("🚥 LEDs: DESLIGADOS")
    
    def cleanup(self):
        """
        Finaliza simulação de sensores
        """
        logger.info("✨ Simulação de sensores finalizada")


# ==============================================================
# CLIENTE MQTT
# ==============================================================

class MQTTClient:
    """
    Cliente MQTT para publicar dados dos sensores
    """
    
    def __init__(self, broker=MQTT_BROKER, port=MQTT_PORT, topic=MQTT_TOPIC):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()
        self.connected = False
        
        # Configurar callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
    
    def on_connect(self, client, userdata, flags, rc):
        """
        Callback de conexão MQTT
        """
        if rc == 0:
            self.connected = True
            logger.info(f"✅ Conectado ao broker MQTT: {self.broker}:{self.port}")
        else:
            self.connected = False
            logger.error(f"❌ Falha na conexão MQTT. Código: {rc}")
    
    def on_disconnect(self, client, userdata, rc):
        """
        Callback de desconexão MQTT
        """
        self.connected = False
        if rc != 0:
            logger.warning("⚠️ Desconexão inesperada do MQTT")
        else:
            logger.info("🔌 Desconectado do MQTT")
    
    def on_publish(self, client, userdata, mid):
        """
        Callback de publicação MQTT
        """
        logger.debug(f"📤 Mensagem publicada - ID: {mid}")
    
    def conectar(self):
        """
        Conecta ao broker MQTT
        """
        try:
            logger.info(f"🔌 Conectando ao MQTT broker: {self.broker}:{self.port}")
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            
            # Aguardar conexão
            timeout = 10
            while not self.connected and timeout > 0:
                time.sleep(0.5)
                timeout -= 0.5
            
            if not self.connected:
                raise Exception("Timeout na conexão MQTT")
                
        except Exception as e:
            logger.error(f"❌ Erro ao conectar MQTT: {e}")
            self.connected = False
    
    def publicar(self, dados):
        """
        Publica dados no tópico MQTT
        """
        if not self.connected:
            logger.error("❌ MQTT não conectado")
            return False
        
        try:
            payload = json.dumps(dados)
            result = self.client.publish(self.topic, payload)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"📤 Dados publicados: {payload}")
                return True
            else:
                logger.error(f"❌ Erro ao publicar dados: {result.rc}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao publicar dados: {e}")
            return False
    
    def desconectar(self):
        """
        Desconecta do broker MQTT
        """
        try:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("🔌 MQTT desconectado")
        except Exception as e:
            logger.error(f"❌ Erro ao desconectar MQTT: {e}")


# ==============================================================
# APLICAÇÃO PRINCIPAL
# ==============================================================

class AplicacaoSensores:
    """
    Aplicação principal para leitura e envio de dados dos sensores
    """
    
    def __init__(self):
        self.sensores = SensorGPIO()
        self.mqtt = MQTTClient()
        self.rodando = False
    
    def iniciar(self):
        """
        Inicia a aplicação
        """
        logger.info("🚀 === INICIANDO APLICAÇÃO DE SENSORES ===")
        logger.info(f"📡 MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
        logger.info(f"📨 Tópico: {MQTT_TOPIC}")
        
        # Conectar ao MQTT
        self.mqtt.conectar()
        
        if not self.mqtt.connected:
            logger.error("❌ Falha na conexão MQTT. Encerrando aplicação.")
            return
        
        self.rodando = True
        self.sensores.controlar_leds(verde=True)
        
        logger.info("✅ Aplicação iniciada! Publicando dados a cada 5 segundos...")
        
        try:
            self.loop_principal()
        except KeyboardInterrupt:
            logger.info("⏹️ Aplicação interrompida pelo usuário")
        finally:
            self.parar()
    
    def loop_principal(self):
        """
        Loop principal da aplicação
        """
        while self.rodando:
            try:
                # Ler dados dos sensores (equivale ao loop() do Arduino)
                temperatura, umidade = self.sensores.ler_temperatura_umidade()
                luminosidade = self.sensores.ler_luminosidade()
                
                # Preparar dados para envio (equivale ao Serial.println() + WiFi.send())
                dados = {
                    "timestamp": datetime.now().isoformat(),
                    "device_id": "raspberry_pi_001",
                    "temperatura": temperatura,
                    "umidade": umidade,
                    "luminosidade": luminosidade
                }
                
                # Filtrar valores None
                dados_limpos = {k: v for k, v in dados.items() if v is not None}
                
                # Publicar dados
                sucesso = self.mqtt.publicar(dados_limpos)
                
                # Controlar LEDs baseado no sucesso
                if sucesso:
                    self.sensores.controlar_leds(verde=True, vermelho=False)
                else:
                    self.sensores.controlar_leds(verde=False, vermelho=True)
                
                # Aguardar próxima leitura
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"❌ Erro no loop principal: {e}")
                self.sensores.controlar_leds(verde=False, vermelho=True)
                time.sleep(5)
    
    def parar(self):
        """
        Para a aplicação
        """
        logger.info("🔧 Parando aplicação...")
        self.rodando = False
        
        # Desconectar MQTT
        self.mqtt.desconectar()
        
        # Limpar GPIO
        self.sensores.controlar_leds(verde=False, vermelho=False)
        self.sensores.cleanup()
        
        logger.info("✅ Aplicação encerrada!")


# ==============================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================

def main():
    """
    Função principal
    """
    print("🚀 === RASPBERRY PI - SENSORES MQTT ===")
    print("Este script lê sensores GPIO e publica via MQTT")
    print("Pressione Ctrl+C para parar")
    print()
    
    app = AplicacaoSensores()
    app.iniciar()


if __name__ == "__main__":
    main()