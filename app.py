# app.py

from flask import Flask
from config import Config
from models import db
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)

    from routes.auth import auth_bp
    from routes.user import user_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')

    with app.app_context():
        db.drop_all()
        db.create_all()

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=True)
