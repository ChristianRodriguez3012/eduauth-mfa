# 🎓 EduAuth-MFA — Proyecto Final: Seguridad Informática

## ✍️ Autor
**Christian Omar Rodríguez Huamanñahui**  
Universidad La Salle  
Curso: Seguridad Informática  
Ciclo: 2025-I

---

## 📌 Descripción del proyecto
Este sistema implementa un flujo completo de autenticación segura con verificación en dos pasos (MFA):

- Backend en Python (Flask)
- Autenticación vía JWT (JSON Web Tokens)
- Verificación de identidad con códigos TOTP desde apps como Google Authenticator
- Interfaz web simple en HTML y JavaScript para pruebas sin Postman

---

## 🛠️ Tecnologías usadas
- Python 3.12
- Flask
- JWT (Flask-JWT-Extended)
- SQLite
- PyOTP
- QRCode (para generación de códigos QR)
- HTML, CSS y JS (frontend de pruebas)

---

## ⚙️ Cómo instalar y ejecutar (en Codespaces)

1. Clona el repositorio:

git clone https://github.com/ChristianRodriguez3012/eduauth-mfa.git
cd eduauth-mfa



2. Crea y activa entorno virtual:

python3 -m venv .venv
source .venv/bin/activate



3. Instala dependencias:

pip install -r requirements.txt



4. Ejecuta el script de configuración del frontend:

chmod +x part2.sh
./part2.sh



5. Inicia el servidor:

python app.py


6. Abre en navegador:

- Si estás local: http://localhost:5000
- En Codespaces: abre el puerto público 5000

---

## 🧪 Flujo de uso completo

### 🔹 Paso 1 — Registro
- Ingresa email y contraseña → clic en **Registrar**

### 🔹 Paso 2 — Login
- Si aún no activas MFA, recibirás un `access_token` directamente

### 🔹 Paso 3 — Setup MFA
- Ingresa tu email y clic en **Generar QR**
- Escanéalo con Google Authenticator

### 🔹 Paso 4 — Verificar MFA
- Coloca el código generado por tu app (6 dígitos)
- Clic en **Activar MFA**

### 🔹 Paso 5 — Login MFA
- Ingresa tu email y código TOTP actual
- Se genera un JWT con `"Bearer "` incluido automáticamente
- ¡Listo para copiar!

### 🔹 Paso 6 — Ver Perfil
- Usa el token generado para acceder a una ruta protegida
- Clic en **Ver Perfil** y verás tus datos

---

## ✅ Capturas sugeridas para entregar
- Registro exitoso
- QR generado
- MFA activado correctamente
- JWT generado
- Acceso al perfil protegido

---

## 📁 Estructura del proyecto

- eduauth-mfa/
  - app.py
  - config.py
  - models.py
  - requirements.txt
  - part2.sh
  - static/
    - index.html
  - routes/
    - auth.py
    - user.py
  - eduauth.db (auto generado)


---

## 🔐 Seguridad
Este proyecto está diseñado con fines educativos. Para un entorno productivo se recomienda:

- Servir con HTTPS (SSL)
- Uso de variables de entorno para claves secretas
- Auditoría de intentos fallidos
- Backend detrás de un servidor WSGI (Gunicorn, etc.)

---

## 📌 Conclusiones
Este proyecto demuestra:

- ✅ Manejo de sesiones seguras con JWT
- ✅ Protección de rutas con tokens
- ✅ Activación y validación de MFA
- ✅ Integración TOTP con apps reales
- ✅ Frontend funcional sin herramientas externas

---

¡Gracias por usar EduAuth-MFA! 🚀