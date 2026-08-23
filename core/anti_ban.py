import random
import time
import math

class AntiBanSimulator:
    def __init__(self):
        # Limites de retardo para simular reflejos humanos (en milisegundos)
        self.min_human_delay_ms = 250
        self.max_human_delay_ms = 600

    def apply_human_jitter(self):
        """Genera una pausa aleatoria antes de ejecutar el clic."""
        delay_ms = random.randint(self.min_human_delay_ms, self.max_human_delay_ms)
        delay_seconds = delay_ms / 1000.0
        time.sleep(delay_seconds)
        return delay_ms

    def calculate_human_touch_coordinates(self, base_x, base_y, button_width, button_height):
        """
        Calcula una coordenada 'sucia' simulando la imprecision de un dedo.
        Aplica un desvio de hasta el 20% del tamano del boton desde su centro.
        """
        # Calcular el rango de variacion (20% del tamano del boton)
        deviation_x = button_width * 0.20
        deviation_y = button_height * 0.20

        # Generar un desplazamiento aleatorio dentro de ese rango
        offset_x = random.uniform(-deviation_x, deviation_x)
        offset_y = random.uniform(-deviation_y, deviation_y)

        # Retornar la coordenada final modificada (en formato entero)
        human_x = math.floor(base_x + offset_x)
        human_y = math.floor(base_y + offset_y)
        
        return {"x": human_x, "y": human_y}

# Ejemplo de uso local (este bloque no se ejecuta si se importa desde otro archivo)
if __name__ == "__main__":
    simulator = AntiBanSimulator()
    print("Aplicando jitter de retraso humano...")
    delay = simulator.apply_human_jitter()
    print(f"Retraso aplicado: {delay} ms")
    
    # Supongamos que el centro del boton 'Aceptar' esta en X=500, Y=1200
    coord = simulator.calculate_human_touch_coordinates(500, 1200, 200, 50)
    print(f"Coordenada simulada de toque: {coord}")
