from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, LoginAttempt, TrustedIdentity

admin_bp = Blueprint('admin', __name__)  # Este blueprint debe registrarse con prefix /admin

# ✅ Historial de intentos de login
@admin_bp.route('/login-attempts', methods=['GET'])
@jwt_required()
def get_login_attempts():
    user_id = get_jwt_identity()
    admin_user = User.query.get(user_id)

    if not admin_user or admin_user.role != 'admin':
        return jsonify(msg='Acceso denegado: requiere rol de administrador'), 403

    attempts = LoginAttempt.query.order_by(LoginAttempt.timestamp.desc()).limit(100).all()
    result = [
        {
            'email': a.email,
            'success': a.success,
            'timestamp': a.timestamp.isoformat(),
            'ip_address': a.ip_address,
            'user_agent': a.user_agent
        } for a in attempts
    ]
    return jsonify(result), 200

# ✅ Registrar DNI aprobado
@admin_bp.route('/add-identity', methods=['POST'])
@jwt_required()
def add_trusted_identity():
    user_id = get_jwt_identity()
    admin_user = User.query.get(user_id)

    if not admin_user or admin_user.role != 'admin':
        return jsonify(msg="Solo administradores pueden realizar esta acción"), 403

    data = request.get_json()
    dni = data.get("dni")
    role = data.get("approved_role")

    if not dni or not role:
        return jsonify(msg="DNI y rol requeridos"), 400

    if TrustedIdentity.query.filter_by(dni=dni).first():
        return jsonify(msg="Este DNI ya está registrado"), 409

    entry = TrustedIdentity(dni=dni, approved_role=role)
    db.session.add(entry)
    db.session.commit()

    return jsonify(msg="DNI aprobado registrado exitosamente"), 201

# ✅ Obtener lista de DNIs aprobados
@admin_bp.route('/trusted-identities', methods=['GET'])
@jwt_required()
def get_trusted_identities():
    user_id = get_jwt_identity()
    admin_user = User.query.get(user_id)

    if not admin_user or admin_user.role != 'admin':
        return jsonify(msg="Solo administradores pueden acceder a esta información"), 403

    identities = TrustedIdentity.query.order_by(TrustedIdentity.created_at.desc()).all()
    result = [
        {
            "dni": t.dni,
            "approved_role": t.approved_role,
            "registrado_en": t.created_at.isoformat()
        } for t in identities
    ]
    return jsonify(result), 200

# ✅ Eliminar un DNI aprobado
@admin_bp.route('/delete-identity', methods=['DELETE'])
@jwt_required()
def delete_trusted_identity():
    user_id = get_jwt_identity()
    admin_user = User.query.get(user_id)

    if not admin_user or admin_user.role != 'admin':
        return jsonify(msg="No autorizado"), 403

    data = request.get_json()
    dni = data.get("dni")
    if not dni:
        return jsonify(msg="DNI requerido"), 400

    record = TrustedIdentity.query.filter_by(dni=dni).first()
    if not record:
        return jsonify(msg="DNI no encontrado"), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify(msg=f"DNI {dni} eliminado correctamente"), 200

# ✅ Actualizar rol de un DNI aprobado
@admin_bp.route('/update-identity-role', methods=['PUT'])
@jwt_required()
def update_identity_role():
    user_id = get_jwt_identity()
    admin_user = User.query.get(user_id)

    if not admin_user or admin_user.role != 'admin':
        return jsonify(msg="No autorizado"), 403

    data = request.get_json()
    dni = data.get("dni")
    new_role = data.get("approved_role")

    if not dni or not new_role:
        return jsonify(msg="DNI y nuevo rol requeridos"), 400

    record = TrustedIdentity.query.filter_by(dni=dni).first()
    if not record:
        return jsonify(msg="DNI no encontrado"), 404

    record.approved_role = new_role
    db.session.commit()
    return jsonify(msg=f"Rol del DNI {dni} actualizado a '{new_role}'"), 200

# ✅ Lista de estudiantes registrados
@admin_bp.route('/student-identities', methods=['GET'])
@jwt_required()
def list_students():
    user_id = get_jwt_identity()
    admin_user = User.query.get(user_id)

    if not admin_user or admin_user.role != 'admin':
        return jsonify(msg='No autorizado'), 403

    students = User.query.filter_by(role='student').all()
    return jsonify([
        {
            "email": s.email,
            "dni": s.dni,
            "created_at": s.created_at.isoformat()
        } for s in students
    ]), 200
