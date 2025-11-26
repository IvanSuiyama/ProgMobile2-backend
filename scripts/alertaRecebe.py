import time
import json
from service.AlertaService import AlertaService
import paho.mqtt.client as mqtt

# Configurações do MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "raspberry/alertas"

# Função para buscar alertas não enviados

def buscar_alertas_nao_enviados(alerta_service, enviados):
    alertas = alerta_service.get_all_alertas()
    novos = [a for a in alertas if a.id not in enviados]
    return novos

def main():
    alerta_service = AlertaService()
    enviados = set()
    
    # Configurar MQTT
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print(f"Conectado ao broker MQTT {MQTT_BROKER}:{MQTT_PORT}")
    
    print("Monitorando tabela de alertas...")
    while True:
        novos_alertas = buscar_alertas_nao_enviados(alerta_service, enviados)
        for alerta in novos_alertas:
            # Monta o JSON do alerta
            payload = json.dumps({"status": "ATIVADO", "id": alerta.id, "nome": alerta.nome, "data": alerta.data.isoformat() if alerta.data else None})
            print(f"Enviando alerta para o Raspberry Pi: {payload}")
            client.publish(MQTT_TOPIC, payload)
            enviados.add(alerta.id)
        time.sleep(2)  # Pesquisa a cada 2 segundos

if __name__ == "__main__":
    main()
