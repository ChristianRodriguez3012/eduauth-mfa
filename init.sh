#!/usr/bin/env bash
set -e

# Nombre del proyecto (opcional, ajusta si es diferente)
PROJECT_DIR=$(pwd)

echo "👉 Iniciando creación de estructura en ${PROJECT_DIR}"

# 1. Crear entorno virtual
python3 -m venv .venv
echo "  • Entorno virtual .venv listo"

# 2. Crear carpetas
mkdir -p routes
echo "  • Carpeta routes/ creada"

# 3. Crear archivos raíz
for file in app.py config.py models.py requirements.txt; do
  touch "$file"
  echo "  • Archivo $file creado"
done

# 4. Crear archivos de rutas
for route in auth.py user.py; do
  touch "routes/$route"
  echo "  • Archivo routes/$route creado"
done

# 5. Mostrar estructura resultante
echo -e "\n✅ Estructura generada:"
find . -maxdepth 2 | sed 's/^/   /'

# 6. Indicaciones finales
cat <<EOF

Siguientes pasos:
1. Dar permisos de ejecución al script (solo la primera vez):
     chmod +x init.sh

2. Ejecutar el script:
     ./init.sh

3. Activar el entorno virtual:
     source .venv/bin/activate

4. Instalar dependencias y actualizar requirements:
     pip install Flask Flask-SQLAlchemy psycopg2-binary Flask-JWT-Extended pyotp qrcode[pil]
     pip freeze > requirements.txt

¡Ya tienes tu proyecto listo para comenzar con el código! 🚀

EOF
