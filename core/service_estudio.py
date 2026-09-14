from core.rentabilidad_calculator import CalculadoraRentabilidad

def on_new_request(card_data):
    # card_data es lo que sacarias del AccessibilityNode
    recojo = card_data["recojo"]
    viaje = card_data["viaje"]
    tarifa = card_data["tarifa"]
    zona = card_data["zona"]

    calc = CalculadoraRentabilidad()
    r = calc.evaluar(recojo, viaje, tarifa, "12:00", "Monday", zona)

    if r["recomendacion"] == "ACEPTAR":
        print(f"🟢 CUMPLE TODO {zona} S/{tarifa} -> Abriendo detalle + parpadeo verde")
        # card_data["node"].performAction(ACTION_CLICK)  # en Android real
        # crear_overlay_verde(card_data["bounds"]) # parpadeo
        return True
    else:
        print(f"🔴 No cumple {zona}: {r['motivo']}")
        return False

# Test de estudio
if __name__ == "__main__":
    on_new_request({"recojo":1.2,"viaje":8,"tarifa":14,"zona":"Florencia"})
    on_new_request({"recojo":3.0,"viaje":8,"tarifa":10,"zona":"El Porvenir"})
