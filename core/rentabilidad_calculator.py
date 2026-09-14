import json, os
from datetime import datetime

class CalculadoraRentabilidad:
    def __init__(self):
        base_path = os.path.join(os.path.dirname(__file__), '..', 'config')
        with open(os.path.join(base_path, "schedules.json"), "r") as f:
            self.config = json.load(f)
        with open(os.path.join(base_path, "zones_trujillo.json"), "r") as f:
            self.zones = json.load(f)
        # TU DATO REAL DE MOTO
        self.costo_por_km = 0.18  # S/ 0.18 por km recorrido

    def evaluar(self, recojo_km, viaje_km, tarifa_soles, hora_str, dia_str, zona_destino):
        costo_total_combustible = (recojo_km + viaje_km) * self.costo_por_km
        
        if dia_str.capitalize() == self.config["rules"].get("except_day"):
            resultado = {"recomendacion": "RECHAZAR", "motivo": f"Descanso: {dia_str}", "rentabilidad_por_km": 0, "ganancia_neta": -costo_total_combustible}
            self._guardar_historial(recojo_km, viaje_km, tarifa_soles, zona_destino, resultado, costo_total_combustible)
            return resultado

        if recojo_km > self.config["rules"]["max_pickup_distance_km"]:
            resultado = {"recomendacion": "RECHAZAR", "motivo": f"Recojo lejos {recojo_km}km", "rentabilidad_por_km": 0, "ganancia_neta": -costo_total_combustible}
            self._guardar_historial(recojo_km, viaje_km, tarifa_soles, zona_destino, resultado, costo_total_combustible)
            return resultado

        slot = self._get_slot(hora_str)
        if not slot:
            tarifa_real = tarifa_soles / viaje_km if viaje_km else 0
            resultado = {"recomendacion": "REVISAR", "motivo": "Fuera de horario", "rentabilidad_por_km": round(tarifa_real,2), "ganancia_neta": round(tarifa_soles - costo_total_combustible,2)}
            self._guardar_historial(recojo_km, viaje_km, tarifa_soles, zona_destino, resultado, costo_total_combustible)
            return resultado

        multiplicador = 1.0
        for z in self.zones.get("complex_zones", []):
            if z["name"].lower() in zona_destino.lower():
                multiplicador = z.get("penalty_multiplier", 1.0)
                break

        tarifa_minima = slot["min_rate_per_km"] * multiplicador
        tarifa_real = tarifa_soles / viaje_km if viaje_km > 0 else 0
        ganancia_neta = tarifa_soles - costo_total_combustible

        if tarifa_real >= tarifa_minima:
            rec = "ACEPTAR"
            motivo = f"Buena: S/ {tarifa_real:.2f}/km >= mínimo S/ {tarifa_minima:.2f}/km (x{multiplicador})"
        elif tarifa_real >= tarifa_minima * 0.85:
            rec = "NEGOCIAR"
            motivo = f"Regular: pide +S/ {(tarifa_minima * viaje_km - tarifa_soles):.2f}"
        else:
            rec = "RECHAZAR"
            motivo = f"Baja: S/ {tarifa_real:.2f}/km < mínimo S/ {tarifa_minima:.2f}/km"

        resultado = {
            "recomendacion": rec,
            "motivo": motivo,
            "rentabilidad_por_km": round(tarifa_real, 2),
            "minimo_requerido": round(tarifa_minima, 2),
            "costo_combustible": round(costo_total_combustible, 2),
            "ganancia_neta": round(ganancia_neta, 2),
            "zona_multiplicador": multiplicador,
            "franja": slot.get("name", hora_str)
        }
        self._guardar_historial(recojo_km, viaje_km, tarifa_soles, zona_destino, resultado, costo_total_combustible)
        return resultado

    def _get_slot(self, hora_str):
        try:
            t = datetime.strptime(hora_str, "%H:%M").time()
        except:
            return None
        for slot in self.config.get("time_slots", []):
            start = datetime.strptime(slot["start"], "%H:%M").time()
            end = datetime.strptime(slot["end"], "%H:%M").time()
            if start <= end:
                if start <= t <= end:
                    return slot
            else:
                if t >= start or t <= end:
                    return slot
        return None

    def _guardar_historial(self, recojo, viaje, tarifa, zona, resultado, costo_comb):
        log_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'asistente_service.log')
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        linea = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {recojo}km+{viaje}km | S/{tarifa} -> {zona} | {resultado['recomendacion']} | Neto:S/{resultado.get('ganancia_neta',0)} | Comb:S/{round(costo_comb,2)}\n"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(linea)
