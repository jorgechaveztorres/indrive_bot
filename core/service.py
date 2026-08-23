import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.listener import InDriveListener

def run_background_service():
    print("--- INICIANDO SERVICIO BACKGROUND NATIVO INDRIVE BOT ---")
    listener = InDriveListener()
    
    # Bucle de monitoreo continuo en segundo plano
    # Simula la escucha activa de notificaciones y eventos del sistema
    cycle = 1
    while True:
        print(f"\n[BACKGROUND] Ciclo de escucha #{cycle} activo...")
        
        # Simulacion de evento de deteccion de viaje (en produccion aqui entra el lector de notificaciones)
        # Evaluamos con hora y dia actual
        listener.simulate_push_event(
            raw_notification_text="Solicitud detectada en radar local",
            current_time="12:30",
            current_day="Monday"
        )
        
        print("[BACKGROUND] En espera de nueva solicitud... (Durmiendo 30 segundos para ahorro de bateria)")
        time.sleep(30)
        cycle += 1

if __name__ == "__main__":
    try:
        run_background_service()
    except KeyboardInterrupt:
        print("\n[BACKGROUND] Servicio detenido manualmente por Kike.")
