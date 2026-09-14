from core.rentabilidad_calculator import CalculadoraRentabilidad

calc = CalculadoraRentabilidad()

print("=== ASISTENTE DE RENTABILIDAD - TRUJILLO ===")
recojo = float(input("Km de recojo: "))
viaje = float(input("Km de viaje: "))
tarifa = float(input("Tarifa ofrecida S/: "))
hora = input("Hora actual (HH:MM) ej 12:30: ")
dia = input("Día (Monday...Sunday): ")
zona = input("Zona destino ej Florencia de Mora: ")

resultado = calc.evaluar(recojo, viaje, tarifa, hora, dia, zona)
print("\n--- RESULTADO ---")
for k,v in resultado.items():
    print(f"{k}: {v}")
