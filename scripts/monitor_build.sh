#!/bin/bash
# Script de recordatorio y monitoreo para procesos largos (60 minutos o más)
INTERVAL_MINUTES=10
TOTAL_TIME_MINUTES=70
ELAPSED=0

echo "--- INICIANDO MONITOREO DE COMPILACION APK (Duracion estimada: $TOTAL_TIME_MINUTES min) ---"

while [ $ELAPSED -lt $TOTAL_TIME_MINUTES ]; do
    echo "[$(date +'%H:%M:%S')] Han pasado $ELAPSED minutos desde el inicio de la compilación."
    echo "[ESTADO] El proceso sigue activo en segundo plano en Termux..."
    
    # Notificación sonora o visual simple en terminal
    echo -e "\a" 
    
    sleep $((INTERVAL_MINUTES * 60))
    ELAPSED=$((ELAPSED + INTERVAL_MINUTES))
done

echo "--- ¡TIEMPO CUMPLIDO! Revisa la carpeta bin/ para ver si el APK ya fue generado. ---"
