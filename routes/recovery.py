# routes/recovery.py

import secrets
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from models import db, User, PasswordResetToken

recovery_bp = Blueprint('recovery', __name__)

@recovery_bp.route('/request-reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    # Generar token
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=15)

    # Guardar en base de datos
    reset_token = PasswordResetToken(user_id=user.id, token=token, expires_at=expires_at)
    db.session.add(reset_token)
    db.session.commit()

    # En producción: enviar por correo
    return jsonify({
        "msg": "Token generado",
        "reset_token": token  # ⚠️ Mostrar en consola por ahora
    })

@recovery_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    token_entry = PasswordResetToken.query.filter_by(token=token).first()

    if not token_entry or token_entry.expires_at < datetime.utcnow():
        return jsonify({"msg": "Token inválido o expirado"}), 400

    user = User.query.get(token_entry.user_id)
    user.password_hash = User.hash_password(new_password)

    db.session.delete(token_entry)  # eliminar token usado
    db.session.commit()

    return jsonify({"msg": "Contraseña actualizada exitosamente"})
