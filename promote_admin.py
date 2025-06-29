# promote_admin.py
from app import create_app
from models import db, User

app = create_app()

with app.app_context():
    email = input("📧 Ingresa el email del usuario a promover: ").strip()
    user = User.query.filter_by(email=email).first()

    if user:
        user.role = 'admin'
        db.session.commit()
        print(f"✅ Usuario {email} promovido a admin.")
    else:
        print(f"⚠️ Usuario con email {email} no encontrado.")
