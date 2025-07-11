#!/bin/sh

echo "Esperando a que PostgreSQL esté disponible..."

python3 << END 
import socket, time, os

host = os.environ.get('DB_HOST', 'ciudadano-postgres')
port = int(os.environ.get('DB_PORT', 5432))

while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            print('PostgreSQL está disponible.')
            break
    except OSError:
        time.sleep(1)
END

echo "Ejecutando migraciones..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Recolectando archivos estáticos..."
python3 manage.py collectstatic --noinput

echo "Ajustando permisos de /app/staticfiles"
chmod -R 755 /app/staticfiles
chown -R appuser:appuser /app/staticfiles

exec "$@"