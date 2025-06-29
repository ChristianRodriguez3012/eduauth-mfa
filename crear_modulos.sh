#!/bin/bash

mkdir -p components js css

# HTML modularizados
for form in register login setup-mfa verify-mfa login-mfa profile request-reset reset-password login-attempts; do
  touch components/form-$form.html
done

# Archivos JS separados
touch js/main.js js/helpers.js js/register.js js/login.js js/mfa.js js/recovery.js js/profile.js js/attempts.js

# Archivo CSS
cat > css/style.css <<EOF
body { font-family: sans-serif; max-width: 600px; margin: 2rem auto; }
form { margin-bottom: 1.5rem; padding: 1rem; border: 1px solid #ccc; }
input, button, select, textarea { display: block; width: 100%; margin-bottom: .5rem; }
code { background: #eee; padding: .5rem; display: block; word-break: break-all; }
.alert {
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 6px;
  font-weight: bold;
  display: none;
}
.alert.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.alert.error   { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.alert.warn    { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
EOF

echo "✅ Estructura creada."
