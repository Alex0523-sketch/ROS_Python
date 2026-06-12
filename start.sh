#!/bin/sh

echo "========================================"
echo "  DIAGNOSTICO DE ARRANQUE"
echo "========================================"
echo "DATABASE_URL : ${DATABASE_URL:-(NO DEFINIDA)}"
echo "POSTGRES_HOST: ${POSTGRES_HOST:-(NO DEFINIDA)}"
echo "POSTGRES_DB  : ${POSTGRES_DB:-(NO DEFINIDA)}"
echo "SECRET_KEY   : ${SECRET_KEY:+(DEFINIDA)}"
echo "DEBUG        : ${DEBUG:-(NO DEFINIDA)}"
echo "PORT         : ${PORT:-8000}"
echo "========================================"

# Si no hay DATABASE_URL, construirla desde variables individuales
if [ -z "$DATABASE_URL" ]; then
    echo "DATABASE_URL no encontrada, construyendo desde POSTGRES_*..."
    export DATABASE_URL="postgresql://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD:-101606}@${POSTGRES_HOST:-localhost}:${POSTGRES_PORT:-5432}/${POSTGRES_DB:-ROS_db}"
    echo "DATABASE_URL construida: postgresql://${POSTGRES_USER:-postgres}:***@${POSTGRES_HOST:-localhost}:${POSTGRES_PORT:-5432}/${POSTGRES_DB:-ROS_db}"
fi

echo "Ejecutando migraciones..."
python manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo "ERROR: Las migraciones fallaron"
    exit 1
fi

echo "Cargando datos iniciales (roles y usuarios base)..."
python manage.py loaddata users/fixtures/initial_data.json --app users || echo "Fixture ya cargado o sin cambios."

echo "Iniciando gunicorn en puerto ${PORT:-8000}..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
