import io
import base64
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import db, User, LoginAttempt, TrustedIdentity
import pyotp
import qrcode

auth_bp = Blueprint('auth', __name__)

ROLES_CON_MFA_OBLIGATORIA = {'admin', 'profesor'}

def log_login_attempt(email, success):
    attempt = LoginAttempt(
        email=email,
        success=success,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(attempt)
    db.session.commit()

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registra un usuario con email, contraseña, rol y opcionalmente DNI.
    Si el rol es sensible (admin, profesor), se valida el DNI contra la lista autorizada.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'student')
    dni = data.get('dni')

    if not email or not password:
        return jsonify(msg='Email y password requeridos'), 400

    if User.query.filter_by(email=email).first():
        return jsonify(msg='Usuario ya existe'), 400

    # Validación adicional si el rol requiere MFA
    if role in ROLES_CON_MFA_OBLIGATORIA:
        if not dni:
            return jsonify(msg=f'Se requiere DNI para el rol "{role}"'), 403

        # Verificar si el DNI ya fue usado
        if User.query.filter_by(dni=dni).first():
            return jsonify(msg='Este DNI ya está asignado a otra cuenta'), 409

        # Verificar si el DNI fue aprobado previamente por un admin
        confiable = TrustedIdentity.query.filter_by(dni=dni, approved_role=role).first()
        if not confiable:
            return jsonify(msg=f'El DNI no está aprobado para el rol "{role}"'), 403

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        dni=dni,
        mfa_required=(role in ROLES_CON_MFA_OBLIGATORIA)
    )
    db.session.add(user)
    db.session.commit()

    return jsonify(msg='Registrado con éxito'), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not check_password_hash(user.password_hash, data.get('password', '')):
        log_login_attempt(data.get('email'), False)
        return jsonify(msg='Credenciales inválidas'), 401

    log_login_attempt(user.email, True)

    if user.mfa_enabled or user.mfa_required:
        return jsonify(mfa_required=True), 200

    token = create_access_token(identity=str(user.id))
    return jsonify(access_token=token), 200

@auth_bp.route('/setup-mfa', methods=['POST'])
def setup_mfa():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user:
        return jsonify(msg='Usuario no encontrado'), 404

    secret = pyotp.random_base32()
    user.mfa_secret = secret
    db.session.commit()

    uri = pyotp.TOTP(secret).provisioning_uri(
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
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()

    if not user or not user.mfa_secret:
        log_login_attempt(data.get('email'), False)
        return jsonify(msg='Flujo MFA inválido'), 400

    totp = pyotp.TOTP(user.mfa_secret)
    if not totp.verify(data.get('code', '')):
        log_login_attempt(user.email, False)
        return jsonify(msg='Código MFA inválido'), 401

    if user.mfa_required and not user.mfa_enabled:
        user.mfa_enabled = True
        db.session.commit()

    token = create_access_token(identity=str(user.id))
    log_login_attempt(user.email, True)
    return jsonify(access_token=token), 200
