from fastapi import FastAPI
from routes.sensores_router import router as sensores_router
from routes.usuarios_router import router as usuarios_router
from routes.geral_router import router as geral_router
from all_module.all_router import router as all_router
from routes.alerta_router import router as alerta_router
from controller.ValoresSensorController import router as valores_router

def configure_routes(app: FastAPI):
    """
    Configura todas as rotas da aplicação
    """
    
    # Incluir rotas gerais
    app.include_router(geral_router)
    
    # Incluir rotas de sensores
    app.include_router(sensores_router)
    
    # Incluir rotas de usuários
    app.include_router(usuarios_router)
    
    # Incluir rotas de dados JSON (MQTT)
    app.include_router(all_router)
    
    # Incluir rotas de alertas
    app.include_router(alerta_router)
    
    # Incluir rotas de valores dos sensores
    app.include_router(valores_router)
    
    # Rota principal (fora dos prefixos)
    @app.get("/")
    async def root():
        """Rota raiz da API"""
        return {
            "message": "Bem-vindo à API de Sensores e Usuários!",
            "version": "1.0.0",
            "documentation": "/docs",
            "endpoints": {
                "sensores": "/sensores",
                "usuarios": "/usuarios",
                "valores": "/valores",
                "alertas": "/alertas",
                "api_geral": "/api"
            }
        }