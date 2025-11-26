from fastapi import APIRouter, HTTPException
from service.AlertaService import AlertaService

router = APIRouter(prefix="/alertas", tags=["Alertas"])

@router.get("/", summary="Listar todos os alertas")
def listar_alertas():
    service = AlertaService()
    alertas = service.get_all_alertas()
    return [a.to_dict() for a in alertas]

@router.get("/{alerta_id}", summary="Obter alerta por ID")
def obter_alerta(alerta_id: int):
    service = AlertaService()
    alerta = service.get_alerta_by_id(alerta_id)
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")
    return alerta.to_dict()

@router.post("/", summary="Criar novo alerta")
def criar_alerta(alerta: dict):
    service = AlertaService()
    novo_alerta = service.create_alerta(alerta)
    return novo_alerta.to_dict()

@router.put("/{alerta_id}", summary="Atualizar alerta")
def atualizar_alerta(alerta_id: int, alerta: dict):
    service = AlertaService()
    alerta_atualizado = service.update_alerta(alerta_id, alerta)
    if not alerta_atualizado:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")
    return alerta_atualizado.to_dict()

@router.delete("/{alerta_id}", summary="Deletar alerta")
def deletar_alerta(alerta_id: int):
    service = AlertaService()
    sucesso = service.delete_alerta(alerta_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")
    return {"detail": "Alerta deletado com sucesso"}
