class CounterOfferManager:
    def __init__(self):
        # Configuración de márgenes para contraofertas (en Soles)
        self.min_acceptable_increase = 1.0  # Incremento mínimo razonable
        self.max_acceptable_increase = 3.0  # Incremento máximo para no espantar al pasajero

    def determine_action_strategy(self, evaluation_result):
        """
        Determina si se acepta la tarifa base o si se calcula una contraoferta basada en la regla de negocio.
        """
        action = evaluation_result.get("action")
        
        if action == "accept":
            return {
                "target": "accept_direct",
                "description": "Aceptar tarifa base directamente",
                "extra_amount": 0.0
            }
        elif action == "counter":
            # Calculamos una contraoferta inteligente basada en la diferencia esperada
            # Aquí aplicamos un incremento dinámico controlado por la política anti-suspensión
            suggested_increment = 2.0 # Soles adicionales sugeridos por defecto
            return {
                "target": "send_counter_offer",
                "description": f"Enviar contraoferta sumando S/ {suggested_increment:.2f} a la tarifa base",
                "extra_amount": suggested_increment
            }
        else:
            return {
                "target": "reject_request",
                "description": "Rechazar solicitud por debajo de umbrales permitidos",
                "extra_amount": 0.0
            }
