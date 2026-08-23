import json
from datetime import datetime

class InDriveEngine:
    def __init__(self):
        with open("config/schedules.json", "r") as f:
            self.config = json.load(f)
        with open("config/zones_trujillo.json", "r") as f:
            self.zones = json.load(f)

    def evaluate_request(self, pickup_distance, trip_distance, total_fare, current_time, current_day, destination_zone):
        if current_day == self.config["rules"]["except_day"]:
            return {"action": "reject", "reason": "Saturday restriction"}

        if pickup_distance > self.config["rules"]["max_pickup_distance_km"]:
            return {"action": "reject", "reason": "Pickup distance exceeds 2km"}

        current_slot = self._get_time_slot(current_time)
        if not current_slot:
            return {"action": "reject", "reason": "Out of schedule"}

        min_rate = current_slot["min_rate_per_km"]

        multiplier = 1.0
        for zone in self.zones["complex_zones"]:
            if zone["name"] == destination_zone:
                multiplier = zone["penalty_multiplier"]
                break

        adjusted_min_rate = min_rate * multiplier
        calculated_rate = total_fare / trip_distance if trip_distance > 0 else 0

        if calculated_rate >= adjusted_min_rate:
            return {"action": "accept", "mode": "direct"}
        elif calculated_rate >= (adjusted_min_rate * 0.85):
            return {"action": "counter_offer", "target_button": 1}
        else:
            return {"action": "reject", "reason": "Below minimum adjusted rate"}

    def _get_time_slot(self, time_str):
        t = datetime.strptime(time_str, "%H:%M").time()
        for slot in self.config["time_slots"]:
            start = datetime.strptime(slot["start"], "%H:%M").time()
            end = datetime.strptime(slot["end"], "%H:%M").time()
            if start <= end:
                if start <= t <= end:
                    return slot
            else:
                if t >= start or t <= end:
                    return slot
        return None
