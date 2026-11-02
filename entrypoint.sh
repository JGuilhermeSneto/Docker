#!/bin/sh
set -e

echo "🐳 [Docker Entrypoint] Inicializando CloudPulse Backend..."

# Aguarda ou executa migrações do banco de dados
echo "⚙️ [Django] Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

# Popula dados demonstrativos caso necessário
echo "🌱 [Django] Verificando dados iniciais..."
python manage.py seed_data || true

echo "🚀 [Docker] Iniciando servidor de aplicação..."
exec "$@"

