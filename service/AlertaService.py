from sqlalchemy.orm import Session
from model.alertaModel import Alerta
from config.databaseConfig import SessionLocal

class AlertaService:
    def __init__(self):
        self.db: Session = SessionLocal()

    def get_all_alertas(self):
        return self.db.query(Alerta).all()

    def get_alerta_by_id(self, alerta_id: int):
        return self.db.query(Alerta).filter(Alerta.id == alerta_id).first()

    def create_alerta(self, alerta_data: dict):
        alerta = Alerta(nome=alerta_data["nome"])
        self.db.add(alerta)
        self.db.commit()
        self.db.refresh(alerta)
        return alerta

    def update_alerta(self, alerta_id: int, alerta_data: dict):
        alerta = self.get_alerta_by_id(alerta_id)
        if not alerta:
            return None
        if "nome" in alerta_data:
            alerta.nome = alerta_data["nome"]
        self.db.commit()
        self.db.refresh(alerta)
        return alerta

    def delete_alerta(self, alerta_id: int):
        alerta = self.get_alerta_by_id(alerta_id)
        if not alerta:
            return False
        self.db.delete(alerta)
        self.db.commit()
        return True
