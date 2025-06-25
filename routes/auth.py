# routes/auth.py

import io
import base64
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import db, User
import pyotp
import qrcode

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registra un usuario con email y contraseña.
    """
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify(msg='Email y password requeridos'), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify(msg='Usuario ya existe'), 400

    pwd_hash = generate_password_hash(data['password'])
    user = User(email=data['email'], password_hash=pwd_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify(msg='Registrado con éxito'), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login básico: si el usuario tiene MFA activado devuelve mfa_required=True,
    si no devuelve el JWT.
    """
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not check_password_hash(user.password_hash, data.get('password', '')):
        return jsonify(msg='Credenciales inválidas'), 401

    if user.mfa_enabled:
        # Indica al frontend que solicite el código TOTP
        return jsonify(mfa_required=True), 200

    # Sin MFA: emite el token directamente
    token = create_access_token(identity=user.id)
    return jsonify(access_token=token), 200


@auth_bp.route('/setup-mfa', methods=['POST'])
def setup_mfa():
    """
    Genera un nuevo secreto TOTP y el QR en base64 para que el usuario lo escanee.
    """
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user:
        return jsonify(msg='Usuario no encontrado'), 404

    # Generar nuevo secreto y guardarlo
    secret = pyotp.random_base32()
    user.mfa_secret = secret
    db.session.commit()

    # Crear QR con URI compatible Google Authenticator
    uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.email,
        issuer_name=current_app.config.get('JWT_SECRET_KEY', 'EduAuth-MFA')
    )
    img = qrcode.make(uri)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    qr_b64 = base64.b64encode(buffered.getvalue()).decode()

    return jsonify(secret=secret, qr_code=f"data:image/png;base64,{qr_b64}"), 200


@auth_bp.route('/verify-mfa', methods=['POST'])
def verify_mfa():
    """
    Verifica el código TOTP enviado por el usuario y activa MFA si es correcto.
    """
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.mfa_secret:
        return jsonify(msg='Usuario o secreto MFA no encontrado'), 404

    totp = pyotp.TOTP(user.mfa_secret)
    if totp.verify(data.get('code', '')):
        user.mfa_enabled = True
        db.session.commit()
        return jsonify(msg='MFA activado correctamente'), 200

    return jsonify(msg='Código MFA inválido'), 401


@auth_bp.route('/login-mfa', methods=['POST'])
def login_mfa():
    """
    Endpoint que recibe email + código TOTP en el flujo de login con MFA.
    Si es válido, emite el JWT.
    """
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.mfa_enabled or not user.mfa_secret:
        return jsonify(msg='Flujo MFA inválido'), 400

    totp = pyotp.TOTP(user.mfa_secret)
    if not totp.verify(data.get('code', '')):
        return jsonify(msg='Código MFA inválido'), 401

    # Código válido: emitir token
    token = create_access_token(identity=str(user.id))
    return jsonify(access_token=token), 200
