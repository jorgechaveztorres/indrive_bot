#!/bin/bash
cd "$(dirname "$0")/.."
pkill -f core/service.py
nohup python3 core/service.py > logs/bot_service.log 2>&1 &
echo "¡InDrive Bot desplegado en el mundo real con éxito, Kike!"
echo "Para ver la actividad en tiempo real, ejecuta: tail -f logs/bot_service.log"
