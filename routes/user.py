# routes/user.py

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User

# Definimos el Blueprint
user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """
    Devuelve información del usuario autenticado.
    """
    uid = get_jwt_identity()
    user = User.query.get(uid)
    return jsonify(
        email=user.email,
        mfa_enabled=user.mfa_enabled,
        created_at=user.created_at.isoformat()
    ), 200

@user_bp.route('/admin', methods=['GET'])
@jwt_required()
def admin_panel():
    """
    Ejemplo de ruta solo para admins.
    """
    user = User.query.get(get_jwt_identity())
    # Suponemos que User tiene un atributo `role` (añádelo si aún no lo tienes)
    if getattr(user, 'role', 'student') != 'admin':
        return jsonify(msg='No autorizado: solo admins'), 403

    return jsonify(secret_data='🚀 Bienvenido, Admin!'), 200
