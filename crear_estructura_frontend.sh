#!/bin/bash

# Crear carpetas base
mkdir -p static/js
mkdir -p static/components

# Formularios a modularizar
formularios=(
  "register"
  "login"
  "setup-mfa"
  "verify-mfa"
  "login-mfa"
  "profile"
  "request-reset"
  "reset-password"
  "login-attempts"
)

# Crear archivos HTML y JS para cada formulario
for nombre in "${formularios[@]}"; do
  html="static/components/$nombre.html"
  js="static/js/$nombre.js"

  # Crear HTML base
  echo "<!-- Formulario: $nombre -->" > "$html"
  echo "<form id=\"form-$nombre\">" >> "$html"
  echo "  <h2>$nombre</h2>" >> "$html"
  echo "</form>" >> "$html"

  # Crear JS base
  echo "// Script para $nombre" > "$js"
  echo "document.getElementById('form-$nombre')?.addEventListener('submit', async (e) => {" >> "$js"
  echo "  e.preventDefault();" >> "$js"
  echo "  // TODO: lógica para $nombre" >> "$js"
  echo "});" >> "$js"
done

echo "✅ Estructura creada en static/components y static/js"
