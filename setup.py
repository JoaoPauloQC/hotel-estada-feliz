"""
SETUP RÁPIDO - Execute este arquivo para criar o admin padrão
python setup_admin.py
"""

from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
from src.database import engine
from src.Model.models import Usuario, Perfil

SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

print("🚀 Iniciando setup do administrador...")
print("-" * 50)

try:
    # 1. Criar perfil Admin
    perfil_admin = db.query(Perfil).filter(Perfil.nome_perfil == "Admin").first()
    if not perfil_admin:
        perfil_admin = Perfil(nome_perfil="Admin")
        db.add(perfil_admin)
        db.commit()
        print("✅ Perfil 'Admin' criado")
    else:
        print("ℹ️  Perfil 'Admin' já existe")
    
    # 2. Criar perfil Hospede
    perfil_hospede = db.query(Perfil).filter(Perfil.nome_perfil == "Hospede").first()
    if not perfil_hospede:
        perfil_hospede = Perfil(nome_perfil="Hospede")
        db.add(perfil_hospede)
        db.commit()
        print("✅ Perfil 'Hospede' criado")
    else:
        print("ℹ️  Perfil 'Hospede' já existe")
    
    # 3. Criar usuário admin
    admin_existe = db.query(Usuario).filter(Usuario.email == "admin@hotelestada.com").first()
    
    if admin_existe:
        print("\n⚠️  ATENÇÃO: Admin já existe!")
        print(f"   Email: admin@hotelestada.com")
        print(f"   Use a senha que você já cadastrou")
    else:
        novo_admin = Usuario(
            nome_completo="Administrador do Sistema",
            email="admin@hotelestada.com",
            senha_hash=generate_password_hash("senha123"),
            perfil_id=perfil_admin.id
        )
        db.add(novo_admin)
        db.commit()
        
        print("\n" + "=" * 50)
        print("✅ ADMINISTRADOR CRIADO COM SUCESSO!")
        print("=" * 50)
        print("\n📧 Email: admin@hotelestada.com")
        print("🔑 Senha: senha123")
        print("\n🌐 Acesse: http://localhost:5000/")
        print("=" * 50)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    db.rollback()
finally:
    db.close()

print("\n✨ Setup concluído!")