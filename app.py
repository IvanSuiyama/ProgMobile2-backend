from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import asyncio

# Importações locais
from config.databaseConfig import create_tables
from model.sensoresModel import criar_tabela_sensores
from all_module.allModel import criar_tabela_all
from scripts.router import configure_routes
from mqtt_module.MQTTService import configure_mqtt_service, start_mqtt_service, stop_mqtt_service


# ==============================================================
# LIFESPAN: executa na inicialização e encerramento do FastAPI
# ==============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --------------------------
    # STARTUP (inicialização)
    # --------------------------
    print("🔧 Configurando banco de dados...")
    create_tables()
    print("✅ Banco de dados configurado!")

    # --------------------------
    # Configurar e iniciar MQTT
    # --------------------------
    print("🔧 Configurando serviço MQTT...")
    configure_mqtt_service(
        host="localhost",  # MQTT broker local no Raspberry Pi
        port=1883,
        topic="raspberry/sensores"  # Novo tópico para dados do Raspberry Pi
    )

    print("✅ Serviço MQTT configurado!")

    # Iniciar o MQTT em background (thread separada)
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, start_mqtt_service)
    print("🚀 Serviço MQTT iniciado em background!")

    # Libera o controle para o FastAPI
    yield

    # --------------------------
    # SHUTDOWN (encerramento)
    # --------------------------
    print("🔧 Parando serviço MQTT...")
    await stop_mqtt_service()
    print("✅ Serviço MQTT parado!")


# ==============================================================
# CRIAÇÃO DA APLICAÇÃO FASTAPI
# ==============================================================

app = FastAPI(
    title="API de Sensores e Usuários",
    description="API REST para gerenciamento de sensores IoT e usuários",
    version="1.0.0",
    lifespan=lifespan
)

# Configura todas as rotas da aplicação
configure_routes(app)


# ==============================================================
# EXECUÇÃO (apenas se for o módulo principal)
# ==============================================================

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",  # Aceita conexões de qualquer IP da rede
        port=8000,
        reload=True,
        log_level="info"
    )
