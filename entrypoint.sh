#!/bin/bash

echo "🚀 Aplicando migrações..."
python manage.py migrate

echo "✅ Iniciando servidor Django"
exec python manage.py runserver 0.0.0.0:8080
