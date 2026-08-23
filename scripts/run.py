import sys
import os

# Asegurar que la ruta base del proyecto este en el path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.engine import InDriveEngine
from core.anti_ban import AntiBanSimulator
from core.counter_offer import CounterOfferManager

def main():
    print('--- INICIALIZANDO SIMULACION INDRIVE BOT (TRUJILLO) ---')
    engine = InDriveEngine()
    anti_ban = AntiBanSimulator()
    counter_manager = CounterOfferManager()

    # Simulacion de una solicitud entrante (Ejemplo: Viaje hacia Florencia de Mora a las 12:00 PM)
    test_pickup_dist = 1.2   # 1.2 km de recojo (Pasa el filtro de <= 2km)
    test_trip_dist = 8.0     # 8 km de recorrido total
    test_fare = 14.0         # Tarifa de 14 soles (~1.75 soles por km)
    test_time = '12:00'      # Horario de almuerzo
    test_day = 'Monday'      # Lunes (No es sabado)
    test_zone = 'Florencia de Mora' # Zona compleja (aplica multiplicador)

    print(f'Evaluando solicitud: Recojo={test_pickup_dist}km, Destino={test_zone}, Tarifa={test_fare} Soles, Hora={test_time}')

    # 1. Evaluar reglas de negocio y geocercas
    eval_result = engine.evaluate_request(
        test_pickup_dist, test_trip_dist, test_fare, test_time, test_day, test_zone
    )
    print(f'Resultado del motor: {eval_result}')

    # 2. Determinar estrategia de botones (Aceptar directo o Contraoferta)
    strategy = counter_manager.determine_action_strategy(eval_result)
    print(f'Estrategia tactica: {strategy}')

    # 3. Si la accion no es rechazar, aplicar jitter anti-ban
    if eval_result['action'] != 'reject':
        print('Aplicando seguridad Anti-Ban (Jitter humano)...')
        delay = anti_ban.apply_human_jitter()
        print(f'¡Accion ejecutada con exito tras {delay} ms de retraso biologico simulado!')
    else:
        print('Solicitud descartada limpiamente por los filtros.')

if __name__ == '__main__':
    main()
