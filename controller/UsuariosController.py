from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from config.databaseConfig import get_database
from service.UsuariosService import UsuariosService
from typing import List, Optional

class UsuariosController:
    """
    Controller para endpoints de Usuários
    """
    
    @staticmethod
    async def listar_usuarios(db: Session = Depends(get_database)) -> List[dict]:
        """
        Lista todos os usuários
        """
        try:
            service = UsuariosService(db)
            usuarios = service.listar_todos()
            return [usuario.to_dict() for usuario in usuarios]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def obter_usuario(usuario_id: int, db: Session = Depends(get_database)) -> dict:
        """
        Obtém um usuário específico por ID
        """
        try:
            service = UsuariosService(db)
            usuario = service.buscar_por_id(usuario_id)
            
            if usuario is None:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            
            return usuario.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def obter_usuario_por_email(email: str, db: Session = Depends(get_database)) -> dict:
        """
        Obtém um usuário por email
        """
        try:
            if not email:
                raise HTTPException(status_code=400, detail="Email é obrigatório")
            
            service = UsuariosService(db)
            usuario = service.buscar_por_email(email)
            
            if usuario is None:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            
            return usuario.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def criar_usuario(
        nome: str,
        email: str,
        senha: str,
        db: Session = Depends(get_database)
    ) -> dict:
        """
        Cria um novo usuário
        """
        try:
            # Validações básicas
            if not nome or not email or not senha:
                raise HTTPException(status_code=400, detail="Nome, email e senha são obrigatórios")
            
            if len(senha) < 6:
                raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 6 caracteres")
            
            if "@" not in email:
                raise HTTPException(status_code=400, detail="Email inválido")
            
            service = UsuariosService(db)
            novo_usuario = service.criar(nome, email, senha)
            
            return novo_usuario.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            if "Email já cadastrado" in str(e):
                raise HTTPException(status_code=409, detail="Email já cadastrado")
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def atualizar_usuario(
        usuario_id: int,
        nome: Optional[str] = None,
        email: Optional[str] = None,
        senha: Optional[str] = None,
        db: Session = Depends(get_database)
    ) -> dict:
        """
        Atualiza um usuário existente
        """
        try:
            # Validações básicas
            if email is not None and "@" not in email:
                raise HTTPException(status_code=400, detail="Email inválido")
            
            if senha is not None and len(senha) < 6:
                raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 6 caracteres")
            
            service = UsuariosService(db)
            usuario_atualizado = service.atualizar(usuario_id, nome, email, senha)
            
            if usuario_atualizado is None:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            
            return usuario_atualizado.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            if "Email já cadastrado" in str(e):
                raise HTTPException(status_code=409, detail="Email já cadastrado")
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def deletar_usuario(usuario_id: int, db: Session = Depends(get_database)) -> dict:
        """
        Deleta um usuário
        """
        try:
            service = UsuariosService(db)
            sucesso = service.deletar(usuario_id)
            
            if not sucesso:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            
            return {"message": f"Usuário {usuario_id} deletado com sucesso"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def buscar_usuarios_por_nome(nome: str, db: Session = Depends(get_database)) -> List[dict]:
        """
        Busca usuários por nome
        """
        try:
            if not nome:
                raise HTTPException(status_code=400, detail="Nome é obrigatório para busca")
            
            service = UsuariosService(db)
            usuarios = service.buscar_por_nome(nome)
            return [usuario.to_dict() for usuario in usuarios]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def autenticar_usuario(email: str, senha: str, db: Session = Depends(get_database)) -> dict:
        """
        Autentica um usuário
        """
        try:
            if not email or not senha:
                raise HTTPException(status_code=400, detail="Email e senha são obrigatórios")
            
            service = UsuariosService(db)
            usuario = service.autenticar(email, senha)
            
            if usuario is None:
                raise HTTPException(status_code=401, detail="Credenciais inválidas")
            
            return {
                "message": "Autenticação realizada com sucesso",
                "usuario": usuario.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def verificar_email(email: str, db: Session = Depends(get_database)) -> dict:
        """
        Verifica se um email já existe
        """
        try:
            if not email:
                raise HTTPException(status_code=400, detail="Email é obrigatório")
            
            service = UsuariosService(db)
            existe = service.email_existe(email)
            
            return {"email": email, "existe": existe}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def estatisticas_usuarios(db: Session = Depends(get_database)) -> dict:
        """
        Retorna estatísticas dos usuários
        """
        try:
            service = UsuariosService(db)
            total = service.contar_total()
            
            return {
                "total_usuarios": total
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))