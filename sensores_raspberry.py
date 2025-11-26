#!/usr/bin/env python3
"""
Script para leitura de sensores conectados diretamente ao GPIO do Raspberry Pi
e publicação dos dados via MQTT
"""

import time
import json
import logging
from datetime import datetime
import paho.mqtt.client as mqtt

# Configurações para importar as bibliotecas GPIO
try:
    import RPi.GPIO as GPIO
    import adafruit_dht
    import board
    GPIO_AVAILABLE = True
except ImportError:
    print("⚠️ Bibliotecas GPIO não encontradas. Execute em modo simulação.")
    GPIO_AVAILABLE = False

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
        self.dht_sensor = None
        self.setup_gpio()
        
    def setup_gpio(self):
        """
        Configura os pinos GPIO
        """
        if not GPIO_AVAILABLE:
            logger.warning("GPIO não disponível. Modo simulação ativo.")
            return
            
        try:
            # Configurar modo GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            # LEDs como saída
            GPIO.setup(LED_VERDE_PIN, GPIO.OUT)
            GPIO.setup(LED_VERMELHO_PIN, GPIO.OUT)
            
            # Configurar LDR como entrada (método de tempo RC)
            # Será configurado dinamicamente no método de leitura
            
            # Sensor DHT11 (ao invés de DHT22)
            self.dht_sensor = adafruit_dht.DHT11(getattr(board, f'D{DHT_PIN}'))
            
            # Inicializar LEDs
            GPIO.output(LED_VERDE_PIN, GPIO.LOW)
            GPIO.output(LED_VERMELHO_PIN, GPIO.LOW)
            
            logger.info("✅ GPIO configurado com sucesso!")
            
        except Exception as e:
            logger.error(f"❌ Erro ao configurar GPIO: {e}")
    
    def ler_temperatura_umidade(self):
        """
        Lê temperatura e umidade do sensor DHT22
        """
        if not GPIO_AVAILABLE or not self.dht_sensor:
            # Modo simulação - valores aleatórios
            import random
            return round(20 + random.uniform(-5, 15), 1), round(50 + random.uniform(-20, 30), 1)
        
        try:
            temperatura = self.dht_sensor.temperature
            umidade = self.dht_sensor.humidity
            
            if temperatura is not None and umidade is not None:
                return round(temperatura, 1), round(umidade, 1)
            else:
                logger.warning("⚠️ Falha na leitura do DHT11")
                return None, None
                
        except Exception as e:
            logger.error(f"❌ Erro ao ler DHT11: {e}")
            return None, None
    
    def ler_luminosidade(self):
        """
        Lê luminosidade do sensor LDR usando método RC (tempo de carga)
        Equivale ao analogRead() do Arduino, mas usando tempo ao invés de ADC
        """
        if not GPIO_AVAILABLE:
            # Modo simulação
            import random
            return random.randint(100, 900)
        
        try:
            # Método RC: mede tempo para carregar capacitor através do LDR
            # Equivale ao analogRead() do Arduino
            
            count = 0
            
            # 1. Configurar pino como saída e descarregar capacitor (digitalWrite LOW)
            GPIO.setup(LDR_PIN, GPIO.OUT)
            GPIO.output(LDR_PIN, GPIO.LOW)
            time.sleep(0.1)  # Descarregar completamente
            
            # 2. Configurar como entrada (pinMode INPUT)
            GPIO.setup(LDR_PIN, GPIO.IN)
            
            # 3. Contar tempo até o pino ficar HIGH (digitalRead)
            start_time = time.time()
            while GPIO.input(LDR_PIN) == GPIO.LOW:
                count += 1
                if count > 100000:  # Timeout para evitar loop infinito
                    break
                    
            # Converter contagem em valor similar ao analogRead (0-1023)
            luminosidade = min(count // 100, 1023)
            
            return luminosidade
            
        except Exception as e:
            logger.error(f"❌ Erro ao ler LDR: {e}")
            return 0
    

    
    def controlar_leds(self, verde=False, vermelho=False):
        """
        Controla os LEDs indicadores
        """
        if not GPIO_AVAILABLE:
            return
            
        try:
            GPIO.output(LED_VERDE_PIN, GPIO.HIGH if verde else GPIO.LOW)
            GPIO.output(LED_VERMELHO_PIN, GPIO.HIGH if vermelho else GPIO.LOW)
        except Exception as e:
            logger.error(f"❌ Erro ao controlar LEDs: {e}")
    
    def cleanup(self):
        """
        Limpa configurações GPIO
        """
        if GPIO_AVAILABLE:
            GPIO.cleanup()


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