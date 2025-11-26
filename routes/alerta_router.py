from fastapi import APIRouter
from controller.AlertaController import router as alerta_controller

router = APIRouter()

# Inclui as rotas do controller de alerta
router.include_router(alerta_controller)
