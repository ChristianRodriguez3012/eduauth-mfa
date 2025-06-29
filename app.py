# app.py

from flask import Flask
from config import Config
from models import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Inicializamos Flask-Migrate fuera de create_app
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    # Inicialización de extensiones
    db.init_app(app)
    JWTManager(app)
    migrate.init_app(app, db)

    # Registro de blueprints
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.recovery import recovery_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(recovery_bp, url_prefix='/recovery')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    print("✅ Blueprints registrados correctamente")

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app

# Punto de entrada
if __name__ == '__main__':
    app = create_app()
    print("🚀 Servidor iniciado en modo debug")
    app.run(host='0.0.0.0', port=5000, debug=True)
