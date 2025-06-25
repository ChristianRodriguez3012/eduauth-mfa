#!/usr/bin/env bash
set -e

echo "👉 Creando frontend estático y actualizando app.py…"

# 1. Crear carpeta static
mkdir -p static
echo "  • Carpeta static/ creada"

# 2. Crear static/index.html
cat > static/index.html << 'EOF'
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>EduAuth MFA Demo</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 2rem auto; }
    form { margin-bottom: 1.5rem; padding: 1rem; border: 1px solid #ccc; }
    label, input, button { display: block; width: 100%; margin-bottom: .5rem; }
  </style>
</head>
<body>
  <h1>EduAuth-MFA Demo</h1>

  <form id="form-register"><h2>1. Registro</h2>
    <input name="email" placeholder="Email" required>
    <input name="password" type="password" placeholder="Contraseña" required>
    <button>Registrar</button><pre id="out-register"></pre></form>

  <form id="form-login"><h2>2. Login</h2>
    <input name="email" placeholder="Email" required>
    <input name="password" type="password" placeholder="Contraseña" required>
    <button>Login</button><pre id="out-login"></pre></form>

  <form id="form-setup-mfa"><h2>3. Setup MFA</h2>
    <input name="email" placeholder="Email" required>
    <button>Generar QR</button>
    <img id="qr-img" alt="QR TOTP" style="display:block; margin:1rem 0; max-width:200px;">
    <pre id="out-setup-mfa"></pre></form>

  <form id="form-verify-mfa"><h2>4. Verificar MFA</h2>
    <input name="email" placeholder="Email" required>
    <input name="code" placeholder="Código TOTP" required>
    <button>Activar MFA</button><pre id="out-verify-mfa"></pre></form>

  <form id="form-login-mfa"><h2>5. Login MFA</h2>
    <input name="email" placeholder="Email" required>
    <input name="code" placeholder="Código TOTP" required>
    <button>Login MFA</button><pre id="out-login-mfa"></pre></form>

  <form id="form-profile"><h2>6. Perfil</h2>
    <input name="token" placeholder="Bearer <TOKEN>" required>
    <button>Ver Perfil</button><pre id="out-profile"></pre></form>

  <script>
    const API = window.location.origin;
    async function call(endpoint, data, opts = {}) {
      const res = await fetch(API + endpoint, {
        method: opts.method || 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(opts.auth ? { 'Authorization': opts.auth } : {})
        },
        body: ['GET'].includes(opts.method) ? null : JSON.stringify(data)
      });
      const txt = await res.text();
      try { return JSON.parse(txt); } catch { return txt; }
    }

    document.getElementById('form-register').onsubmit = async e => {
      e.preventDefault();
      const f = e.target;
      const out = await call('/auth/register', { email:f.email.value, password:f.password.value });
      document.getElementById('out-register').innerText = JSON.stringify(out, null, 2);
    };
    document.getElementById('form-login').onsubmit = async e => {
      e.preventDefault();
      const f = e.target;
      const out = await call('/auth/login', { email:f.email.value, password:f.password.value });
      document.getElementById('out-login').innerText = JSON.stringify(out, null, 2);
    };
    document.getElementById('form-setup-mfa').onsubmit = async e => {
      e.preventDefault();
      const f = e.target;
      const out = await call('/auth/setup-mfa', { email:f.email.value });
      document.getElementById('qr-img').src = out.qr_code || '';
      document.getElementById('out-setup-mfa').innerText = JSON.stringify(out, null, 2);
    };
    document.getElementById('form-verify-mfa').onsubmit = async e => {
      e.preventDefault();
      const f = e.target;
      const out = await call('/auth/verify-mfa', { email:f.email.value, code:f.code.value });
      document.getElementById('out-verify-mfa').innerText = JSON.stringify(out, null, 2);
    };
    document.getElementById('form-login-mfa').onsubmit = async e => {
      e.preventDefault();
      const f = e.target;
      const out = await call('/auth/login-mfa', { email:f.email.value, code:f.code.value });
      document.getElementById('out-login-mfa').innerText = JSON.stringify(out, null, 2);
    };
    document.getElementById('form-profile').onsubmit = async e => {
      e.preventDefault();
      const f = e.target;
      const out = await call('/user/profile', {}, { method:'GET', auth:f.token.value });
      document.getElementById('out-profile').innerText = JSON.stringify(out, null, 2);
    };
  </script>
</body>
</html>
EOF
echo "  • static/index.html creado"

# 3. Sobrescribir app.py con código que sirva el HTML
cat > app.py << 'EOF'
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
EOF
echo "  • app.py actualizado"

echo -e "\n✅ Script part2.sh ejecutado con éxito."
echo "   Ejecuta ahora:"
echo "     python app.py"
echo "   Luego abre tu navegador en:"
echo "     http://localhost:5000 (o el enlace público de tu Codespace)"
