#!/bin/bash
# Lanza el bot en segundo plano usando nohup para que no se apague al cerrar Termux
cd "$(dirname "$0")/.."
nohup python3 core/service.py > logs/bot_service.log 2>&1 &
echo "¡Servicio iniciado en segundo plano con éxito, Kike!"
echo "Puedes revisar los registros en tiempo real ejecutando: tail -f logs/bot_service.log"
