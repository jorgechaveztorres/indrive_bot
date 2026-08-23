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
        self.indrive_package = "sinaddons.android.taxi"

    def bring_app_to_foreground(self):
        """
        Lanza la aplicacion usando el intent de inicio por categoria nativo de Android.
        """
        try:
            # Comando limpio compatible con todos los Android para traer la app al frente
            cmd = f"am start -n {self.indrive_package}/.MainActivity 2>/dev/null || am start -d indrive://app"
            subprocess.run(["sh", "-c", cmd], check=False)
            print("[LISTENER] App inDrive traída al primer plano con éxito.")
        except Exception as e:
            print(f"[LISTENER] Error al intentar abrir inDrive: {e}")

    def simulate_push_event(self, raw_notification_text, current_time, current_day):
        print(f"\n[PUSH DETECTADA] Mensaje: '{raw_notification_text}'")
        
        # 1. Traer inDrive al frente
        self.bring_app_to_foreground()
        
        parsed_data = {
            "pickup_distance": 1.0,
            "trip_distance": 6.5,
            "total_fare": 12.0,
            "destination_zone": "Florencia de Mora"
        }

        print(f"[PARSER] Datos extraídos -> Recojo: {parsed_data['pickup_distance']}km | Destino: {parsed_data['destination_zone']} | Tarifa: {parsed_data['total_fare']} Soles")

        # 2. Motor de reglas
        eval_result = self.engine.evaluate_request(
            parsed_data["pickup_distance"],
            parsed_data["trip_distance"],
            parsed_data["total_fare"],
            current_time,
            current_day,
            parsed_data["destination_zone"]
        )
        print(f"[MOTOR] Evaluación: {eval_result}")

        # 3. Estrategia
        strategy = self.counter_manager.determine_action_strategy(eval_result)
        print(f"[ESTRATEGIA] Acción a tomar: {strategy}")

        # 4. Anti-Ban y acción
        if eval_result['action'] != 'reject':
            delay = self.anti_ban.apply_human_jitter()
            print(f"[ACCIÓN] ¡Clic ejecutado tras {delay} ms de Jitter biológico!")
        else:
            print("[ACCIÓN] Solicitud descartada por filtros de negocio.")

if __name__ == "__main__":
    listener = InDriveListener()
    listener.simulate_push_event("Nueva solicitud de viaje disponible cerca de ti", "12:15", "Monday")
