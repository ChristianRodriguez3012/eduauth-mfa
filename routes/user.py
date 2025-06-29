# routes/user.py

from flask import Blueprint, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, LoginAttempt
import os

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
        role=user.role,
        created_at=user.created_at.isoformat()
    ), 200


@user_bp.route('/admin', methods=['GET'])
@jwt_required()
def admin_panel():
    """
    Ejemplo de ruta solo para admins.
    """
    user = User.query.get(get_jwt_identity())
    if not user or user.role != 'admin':
        return jsonify(msg='No autorizado: solo admins'), 403

    return jsonify(secret_data='🚀 Bienvenido, Admin!'), 200


@user_bp.route('/login-attempts', methods=['GET'])
@jwt_required()
def view_login_attempts():
    """
    Devuelve los últimos intentos de acceso. Solo accesible para admins.
    """
    user = User.query.get(get_jwt_identity())
    if not user or user.role != 'admin':
        return jsonify(msg='No autorizado: solo admins'), 403

    attempts = LoginAttempt.query.order_by(LoginAttempt.timestamp.desc()).limit(100).all()
    return jsonify([
        {
            "email": a.email,
            "success": a.success,
            "timestamp": a.timestamp.isoformat(),
            "ip_address": a.ip_address,
            "user_agent": a.user_agent
        } for a in attempts
    ]), 200


@user_bp.route('/admin-dashboard', methods=['GET'])
@jwt_required()
def serve_admin_dashboard():
    """
    Devuelve el panel admin (admin.html) si el usuario autenticado es admin.
    """
    user = User.query.get(get_jwt_identity())
    if not user or user.role != 'admin':
        return jsonify(msg='No autorizado'), 403

    # Ruta absoluta a la carpeta 'static' para servir admin.html
    return send_from_directory(os.path.join(os.getcwd(), 'static'), 'admin.html')
