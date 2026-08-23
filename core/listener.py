import subprocess
import time
import json
from core.engine import InDriveEngine
from core.anti_ban import AntiBanSimulator
from core.counter_offer import CounterOfferManager

class InDriveListener:
    def __init__(self):
        self.engine = InDriveEngine()
        self.anti_ban = AntiBanSimulator()
        self.counter_manager = CounterOfferManager()
        # Nombre del paquete oficial de inDrive (puede variar ligeramente, tipicamente com.indrive)
        self.indrive_package = "sinaddons.android.taxi" # o "android.taxi" segun la version instalada

    def bring_app_to_foreground(self):
        """
        Fuerza a Android a traer la aplicacion de inDrive al primer plano 
        cuando se detecta una solicitud o evento critico.
        """
        try:
            # Comando de ADB / shell nativo de Android para abrir el paquete de la app
            subprocess.run(["am", "start", "-n", f"{self.indrive_package}/md.yambiki.taxi.presentation.splash.SplashActivity"], check=False)
            print("[LISTENER] App inDrive traída al primer plano con éxito.")
        except Exception as e:
            print(f"[LISTENER] Error al intentar abrir inDrive: {e}")

    def simulate_push_event(self, raw_notification_text, current_time, current_day):
        """
        Simula la recepcion de una push, abre la app y procesa la carrera.
        """
        print(f"\n[PUSH DETECTADA] Mensaje: '{raw_notification_text}'")
        
        # 1. Traer inDrive al frente de inmediato
        self.bring_app_to_foreground()
        
        # Simulación de parsing de los datos extraídos de la notificación/pantalla
        # (En la versión final, esto vendrá del lector de nodos de accesibilidad)
        parsed_data = {
            "pickup_distance": 1.0,      # km de recojo
            "trip_distance": 6.5,        # km totales
            "total_fare": 12.0,          # Soles
            "destination_zone": "Florencia de Mora" # Zona evaluada
        }

        print(f"[PARSER] Datos extraídos -> Recojo: {parsed_data['pickup_distance']}km | Destino: {parsed_data['destination_zone']} | Tarifa: {parsed_data['total_fare']} Soles")

        # 2. Pasar por el motor de reglas
        eval_result = self.engine.evaluate_request(
            parsed_data["pickup_distance"],
            parsed_data["trip_distance"],
            parsed_data["total_fare"],
            current_time,
            current_day,
            parsed_data["destination_zone"]
        )
        print(f"[MOTOR] Evaluación: {eval_result}")

        # 3. Determinar estrategia
        strategy = self.counter_manager.determine_action_strategy(eval_result)
        print(f"[ESTRATEGIA] Acción a tomar: {strategy}")

        # 4. Ejecutar Anti-Ban y clic si procede
        if eval_result['action'] != 'reject':
            delay = self.anti_ban.apply_human_jitter()
            print(f"[ACCIÓN] ¡Clic ejecutado tras {delay} ms de Jitter biológico!")
        else:
            print("[ACCIÓN] Solicitud descartada por filtros de negocio.")

if __name__ == "__main__":
    listener = InDriveListener()
    # Prueba simulada de entrada en horario matutino / almuerzo
    listener.simulate_push_event("Nueva solicitud de viaje disponible cerca de ti", "12:15", "Monday")
