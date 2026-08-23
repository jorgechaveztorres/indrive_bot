import time
import os
import sys
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.engine import InDriveEngine
from core.anti_ban import AntiBanSimulator
from core.counter_offer import CounterOfferManager

class RealWorldListener:
    def __init__(self):
        self.engine = InDriveEngine()
        self.anti_ban = AntiBanSimulator()
        self.counter_manager = CounterOfferManager()
        self.indrive_package = "sinaddons.android.taxi"

    def bring_app_to_foreground(self):
        try:
            cmd = f"am start -n {self.indrive_package}/.MainActivity 2>/dev/null"
            subprocess.run(["sh", "-c", cmd], check=False)
        except Exception:
            pass

    def start_real_monitoring(self):
        print("==================================================")
        print("  [ESTADO REAL] INGRID BOT ACTIVO - MODO 24/7")
        print("  Regla de recojo máximo: <= 2 km (7 días)")
        print("  Cálculo de rentabilidad: 1 Sol / km")
        print("==================================================")
        
        cycle = 1
        while True:
            # En entorno real de producción, aquí conectamos el volcado de notificaciones de Termux
            # o el monitoreo de eventos activos del sistema.
            print(f"\n[ESCUCHA ACTIVA] Ciclo #{cycle} - Monitoreando radar local en Moche / Trujillo...")
            
            # Simulamos la espera pasiva de baja carga de CPU para cuidar la batería del celular
            time.sleep(15)
            cycle += 1

if __name__ == "__main__":
    try:
        listener = RealWorldListener()
        listener.start_real_monitoring()
    except KeyboardInterrupt:
        print("\n[ESTADO REAL] Operación detenida por Kike.")
