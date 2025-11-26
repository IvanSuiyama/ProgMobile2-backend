from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from model.usuariosModel import Usuarios
from typing import List, Optional

class UsuariosService:
    """
    Service para operações CRUD de Usuários
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def listar_todos(self) -> List[Usuarios]:
        """
        Lista todos os usuários
        """
        try:
            return self.db.query(Usuarios).all()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao listar usuários: {str(e)}")
    
    def buscar_por_id(self, usuario_id: int) -> Optional[Usuarios]:
        """
        Busca um usuário por ID
        """
        try:
            return self.db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar usuário: {str(e)}")
    
    def buscar_por_email(self, email: str) -> Optional[Usuarios]:
        """
        Busca um usuário por email
        """
        try:
            return self.db.query(Usuarios).filter(Usuarios.email == email).first()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar usuário por email: {str(e)}")
    
    def email_existe(self, email: str) -> bool:
        """
        Verifica se um email já existe
        """
        try:
            return self.db.query(Usuarios).filter(Usuarios.email == email).first() is not None
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao verificar email: {str(e)}")
    
    def criar(self, nome: str, email: str, senha: str) -> Usuarios:
        """
        Cria um novo usuário
        """
        try:
            # Verificar se email já existe
            if self.email_existe(email):
                raise Exception("Email já cadastrado")
            
            novo_usuario = Usuarios(
                nome=nome,
                email=email,
                senha=senha  # Em produção, deveria ser hashada
            )
            
            self.db.add(novo_usuario)
            self.db.commit()
            self.db.refresh(novo_usuario)
            
            return novo_usuario
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao criar usuário: {str(e)}")
    
    def atualizar(self, usuario_id: int, nome: Optional[str] = None, 
                  email: Optional[str] = None, senha: Optional[str] = None) -> Optional[Usuarios]:
        """
        Atualiza um usuário existente
        """
        try:
            usuario = self.db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
            
            if not usuario:
                return None
            
            # Verificar se o novo email já existe (se fornecido)
            if email is not None and email != usuario.email:
                if self.email_existe(email):
                    raise Exception("Email já cadastrado")
            
            # Atualizar apenas campos fornecidos
            if nome is not None:
                usuario.nome = nome
            if email is not None:
                usuario.email = email
            if senha is not None:
                usuario.senha = senha  # Em produção, deveria ser hashada
            
            self.db.commit()
            self.db.refresh(usuario)
            
            return usuario
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao atualizar usuário: {str(e)}")
    
    def deletar(self, usuario_id: int) -> bool:
        """
        Deleta um usuário
        """
        try:
            usuario = self.db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
            
            if not usuario:
                return False
            
            self.db.delete(usuario)
            self.db.commit()
            
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao deletar usuário: {str(e)}")
    
    def contar_total(self) -> int:
        """
        Conta total de usuários
        """
        try:
            return self.db.query(Usuarios).count()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao contar usuários: {str(e)}")
    
    def buscar_por_nome(self, nome: str) -> List[Usuarios]:
        """
        Busca usuários por nome (busca parcial)
        """
        try:
            return self.db.query(Usuarios).filter(Usuarios.nome.contains(nome)).all()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar usuários por nome: {str(e)}")
    
    def autenticar(self, email: str, senha: str) -> Optional[Usuarios]:
        """
        Autentica um usuário
        """
        try:
            return self.db.query(Usuarios).filter(
                Usuarios.email == email, 
                Usuarios.senha == senha  # Em produção, usar hash
            ).first()
        except SQLAlchemyError as e:
            raise Exception(f"Erro na autenticação: {str(e)}")