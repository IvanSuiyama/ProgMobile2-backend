import threading
import json
import logging
from datetime import datetime
from typing import Optional
import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session
from config.databaseConfig import SessionLocal
from all_module.AllService import AllService

# ==============================================================
# CONFIGURAÇÃO DE LOG
# ==============================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==============================================================
# CLASSE PRINCIPAL DO SERVIÇO MQTT
# ==============================================================

class MQTTService:
    """
    Serviço MQTT usando paho-mqtt para receber dados do ESP32 e salvar no banco.
    """

    def __init__(
        self,
        broker_host: str = "localhost",
        broker_port: int = 1883,
        topic: str = "raspberry/sensores",
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.topic = topic
        self.alerta_topic = "raspberry/alertas"
        self.username = username
        self.password = password
        self.client = mqtt.Client()
        self.thread = None
        self.running = False

    # ==============================================================
    # EVENTOS MQTT
    # ==============================================================

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"✅ Conectado ao broker MQTT: {self.broker_host}:{self.broker_port}")
            client.subscribe(self.topic)
            client.subscribe(self.alerta_topic)
            logger.info(f"🎯 Inscrito nos tópicos: {self.topic}, {self.alerta_topic}")
        else:
            logger.error(f"❌ Falha na conexão com o broker. Código de erro: {rc}")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        logger.info(f"📨 Mensagem recebida - Tópico: {topic} | Dados: {payload}")
        self.save_to_database(topic, payload)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning("⚠️ Desconexão inesperada. Tentando reconectar...")
            self.reconnect()
        else:
            logger.info("🔌 Desconectado do broker MQTT")

    # ==============================================================
    # BANCO DE DADOS
    # ==============================================================

    def save_to_database(self, topic: str, payload: str):
        try:
            db = SessionLocal()
            service = AllService(db)
            result = service.criar(topic, payload)

            if result:
                print("\n🎯 === DADOS RECEBIDOS DO RASPBERRY PI ===")
                print(f"🕒 Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"📡 Tópico: {topic}")
                print(f"📦 Dados: {payload}")
                print(f"💾 Salvo no banco - ID: {result.id}")
                print("=" * 40)
                logger.info(f"✅ Dados salvos na tabela 'all' - ID: {result.id}")
            else:
                logger.error("❌ Falha ao salvar no banco de dados")

        except Exception as e:
            logger.error(f"❌ Erro ao salvar no banco: {e}")
        finally:
            db.close()

    # ==============================================================
    # CONTROLE DO SERVIÇO MQTT
    # ==============================================================

    def start(self):
        """
        Inicia o serviço MQTT em uma thread separada (background)
        """
        if self.running:
            logger.warning("⚠️ Serviço MQTT já está em execução.")
            return

        self.running = True
        logger.info("🚀 Iniciando serviço MQTT para Raspberry Pi...")

        # Configura callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        # Credenciais, se houver
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)

        try:
            self.client.connect(self.broker_host, self.broker_port)
            self.thread = threading.Thread(target=self.client.loop_forever, daemon=True)
            self.thread.start()
            logger.info("✅ Serviço MQTT iniciado em background!")
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar serviço MQTT: {e}")
            self.running = False

    def stop(self):
        """
        Para o serviço MQTT e encerra a thread
        """
        if not self.running:
            logger.warning("⚠️ Serviço MQTT não está em execução.")
            return

        logger.info("🔧 Parando serviço MQTT...")
        try:
            self.running = False
            self.client.disconnect()
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=2)
            logger.info("✅ Serviço MQTT parado com sucesso!")
        except Exception as e:
            logger.error(f"❌ Erro ao parar serviço MQTT: {e}")

    def reconnect(self):
        """
        Tenta reconectar ao broker caso a conexão seja perdida
        """
        while self.running:
            try:
                logger.info("🔁 Tentando reconectar ao broker MQTT...")
                self.client.reconnect()
                logger.info("✅ Reconectado com sucesso!")
                return
            except Exception as e:
                logger.error(f"❌ Falha ao reconectar: {e}. Tentando novamente em 5s...")
                import time
                time.sleep(5)


# ==============================================================
# FUNÇÕES DE INTEGRAÇÃO COM O FASTAPI
# ==============================================================

mqtt_service = None


def configure_mqtt_service(
    host: str = "localhost",
    port: int = 1883,
    topic: str = "esp32/sensores",
    username: str = None,
    password: str = None,
):
    """
    Cria e configura o serviço MQTT global.
    """
    global mqtt_service
    mqtt_service = MQTTService(host, port, topic, username, password)
    logger.info(f"🔧 MQTT configurado - Broker: {host}:{port}, Tópico: {topic}")


def start_mqtt_service():
    """
    Inicia o serviço MQTT (síncrono, para rodar em executor ou thread)
    """
    global mqtt_service
    if mqtt_service:
        mqtt_service.start()


def stop_mqtt_service():
    """
    Para o serviço MQTT
    """
    global mqtt_service
    if mqtt_service:
        mqtt_service.stop()
