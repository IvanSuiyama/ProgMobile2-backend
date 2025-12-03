#!/usr/bin/env python3
"""
Script para inicializar dados padrão do sistema.
Cria usuário administrador e configura dados iniciais.
"""

import os
import sys

# Adicionar o diretório pai ao path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.databaseConfig import SessionLocal, create_tables
from service.UsuariosService import UsuariosService
from model.sensoresModel import criar_tabelas_sensores

def criar_usuario_admin():
    """
    Cria o usuário administrador padrão do sistema.
    """
    # Garantir que as tabelas existam
    create_tables()
    criar_tabelas_sensores()
    
    # Criar sessão do banco
    db = SessionLocal()
    
    try:
        # Criar service de usuários
        usuario_service = UsuariosService(db)
        
        # Dados do usuário administrador
        email_admin = "ivan@adm.com"
        nome_admin = "Ivan Administrador"
        senha_admin = "123456"
        
        # Verificar se já existe o usuário admin
        usuario_existente = usuario_service.buscar_por_email(email_admin)
        
        if usuario_existente:
            print(f"✅ Usuário administrador já existe:")
            print(f"   Email: {usuario_existente.email}")
            print(f"   Nome: {usuario_existente.nome}")
            print(f"   ID: {usuario_existente.id}")
        else:
            # Criar usuário administrador
            novo_usuario = usuario_service.criar(
                nome=nome_admin,
                email=email_admin,
                senha=senha_admin
            )
            
            print(f"🎉 Usuário administrador criado com sucesso!")
            print(f"   Email: {novo_usuario.email}")
            print(f"   Nome: {novo_usuario.nome}")
            print(f"   Senha: {senha_admin}")
            print(f"   ID: {novo_usuario.id}")
            
            print("\n📝 Dados para login no app:")
            print(f"   Email: {email_admin}")
            print(f"   Senha: {senha_admin}")
        
        # Mostrar estatísticas
        total_usuarios = usuario_service.contar_total()
        print(f"\n📊 Total de usuários no sistema: {total_usuarios}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário administrador: {str(e)}")
        return False
        
    finally:
        db.close()

def listar_todos_usuarios():
    """
    Lista todos os usuários do sistema.
    """
    db = SessionLocal()
    
    try:
        usuario_service = UsuariosService(db)
        usuarios = usuario_service.listar_todos()
        
        if not usuarios:
            print("📋 Nenhum usuário encontrado no sistema.")
            return
        
        print(f"📋 Usuários cadastrados ({len(usuarios)}):")
        print("-" * 50)
        
        for usuario in usuarios:
            print(f"ID: {usuario.id}")
            print(f"Nome: {usuario.nome}")
            print(f"Email: {usuario.email}")
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ Erro ao listar usuários: {str(e)}")
        
    finally:
        db.close()

def main():
    """
    Função principal do script de inicialização
    """
    print("🚀 === INICIALIZAÇÃO DO SISTEMA ===")
    print("Este script configura dados padrão do sistema:")
    print("- Cria tabelas do banco de dados")
    print("- Cria usuário administrador padrão")
    print("=" * 50)
    
    # Criar usuário administrador
    sucesso = criar_usuario_admin()
    
    if sucesso:
        print("\n" + "=" * 50)
        listar_todos_usuarios()
        print("\n✅ Inicialização concluída com sucesso!")
        print("\n🚀 Sistema pronto para uso!")
        print("\n📱 Dados para login no aplicativo:")
        print("   Email: ivan@adm.com")
        print("   Senha: 123456")
        print("\n💡 Lembre-se de criar sensores pelo frontend!")
    else:
        print("\n❌ Falha na inicialização do sistema.")
        sys.exit(1)

if __name__ == "__main__":
    main()