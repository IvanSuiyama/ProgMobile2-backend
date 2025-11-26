from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.databaseConfig import get_database
from controller.UsuariosController import UsuariosController

# Criar router para usuários
router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"description": "Usuário não encontrado"}}
)

@router.get("/")
async def listar_usuarios(db: Session = Depends(get_database)):
    """Lista todos os usuários"""
    return await UsuariosController.listar_usuarios(db)

@router.get("/{usuario_id}")
async def obter_usuario(usuario_id: int, db: Session = Depends(get_database)):
    """Obtém um usuário específico"""
    return await UsuariosController.obter_usuario(usuario_id, db)

@router.get("/email/{email}")
async def obter_usuario_por_email(email: str, db: Session = Depends(get_database)):
    """Obtém um usuário por email"""
    return await UsuariosController.obter_usuario_por_email(email, db)

@router.post("/")
async def criar_usuario(
    nome: str,
    email: str,
    senha: str,
    db: Session = Depends(get_database)
):
    """Cria um novo usuário"""
    return await UsuariosController.criar_usuario(nome, email, senha, db)

@router.put("/{usuario_id}")
async def atualizar_usuario(
    usuario_id: int,
    nome: str = None,
    email: str = None,
    senha: str = None,
    db: Session = Depends(get_database)
):
    """Atualiza um usuário"""
    return await UsuariosController.atualizar_usuario(usuario_id, nome, email, senha, db)

@router.delete("/{usuario_id}")
async def deletar_usuario(usuario_id: int, db: Session = Depends(get_database)):
    """Deleta um usuário"""
    return await UsuariosController.deletar_usuario(usuario_id, db)

@router.get("/buscar/{nome}")
async def buscar_usuarios_por_nome(nome: str, db: Session = Depends(get_database)):
    """Busca usuários por nome"""
    return await UsuariosController.buscar_usuarios_por_nome(nome, db)

@router.post("/login")
async def login_usuario(email: str, senha: str, db: Session = Depends(get_database)):
    """Autentica um usuário"""
    return await UsuariosController.autenticar_usuario(email, senha, db)

@router.get("/verificar-email/{email}")
async def verificar_email(email: str, db: Session = Depends(get_database)):
    """Verifica se email já existe"""
    return await UsuariosController.verificar_email(email, db)

@router.get("/stats/estatisticas")
async def estatisticas_usuarios(db: Session = Depends(get_database)):
    """Estatísticas dos usuários"""
    return await UsuariosController.estatisticas_usuarios(db)