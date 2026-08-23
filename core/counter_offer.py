class CounterOfferManager:
    def __init__(self):
        # Mapeo de botones de contraoferta segun la interfaz de inDrive
        # Boton principal: Aceptar tarifa actual
        # Boton 1: Primera opcion de incremento
        # Boton 2: Segunda opcion de incremento
        self.available_buttons = {
            "accept_direct": {"action_type": "click", "index": 0},
            "counter_1": {"action_type": "click", "index": 1},
            "counter_2": {"action_type": "click", "index": 2}
        }

    def determine_action_strategy(self, evaluation_result):
        """
        Determina que boton presionar segun el resultado devuelto por el engine.
        """
        action = evaluation_result.get("action")
        
        if action == "accept":
            return {
                "target": "accept_direct",
                "description": "Aceptar tarifa base directamente"
            }
        elif action == "counter_offer":
            target_btn = evaluation_result.get("target_button", 1)
            if target_btn == 1:
                return {
                    "target": "counter_1",
                    "description": "Lanzar primera contraoferta (margen seguro)"
                }
            else:
                return {
                    "target": "counter_2",
                    "description": "Lanzar segunda contraoferta (hora pico / zona compleja)"
                }
        else:
            return {
                "target": "reject",
                "description": "Descartar solicitud"
            }

if __name__ == "__main__":
    manager = CounterOfferManager()
    # Prueba simulada
    fake_eval = {"action": "counter_offer", "target_button": 2}
    strategy = manager.determine_action_strategy(fake_eval)
    print(f"Estrategia seleccionada: {strategy}")
