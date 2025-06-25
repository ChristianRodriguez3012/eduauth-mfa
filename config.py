# config.py

import os

class Config:
    # Clave secreta de Flask (para sesiones, CSRF, etc.)
    SECRET_KEY = os.getenv('SECRET_KEY', 'cambiar-esta-frase-por-una-aleatoria-y-segura')

    # Usaremos SQLite en desarrollo: un archivo en la raíz llamado eduauth.db
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(BASE_DIR, 'eduauth.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clave secreta para JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'otra-frase-secreta-para-jwt')
