import random
from datetime import datetime, timedelta

class ScenarioEngine:
    def __init__(self, scenario_type="fire"):
        self.scenario_id = f"{scenario_type}_scenario"
        self.scenario_type = scenario_type

        self.location_id = "East_Wing"

        self.start_time = None
        self.time = None

        self.zones = {
            "A": 50,
            "B": 30,
            "C": 20
        }

        self.zone_area = {
            "A": 50,
            "B": 40,
            "C": 30
        }

        self.events = []

    def get_density(self, zone_id):
        return self.zones[zone_id] / self.zone_area[zone_id]

    def get_speed(self, density):
        if density < 0.5:
            return 1.0
        elif density < 1.5:
            return 0.8
        elif density < 2.5:
            return 0.6
        elif density < 4.0:
            return 0.4
        else:
            return 0.2

    def check_congestion(self, zone_id):
        density = self.get_density(zone_id)

        if density > 4.0:
            return "CRITICAL_CONGESTION_" + zone_id
        elif density > 2.5:
            return "CONGESTION_" + zone_id
        else:
            return None

    def fire_scenario(self, elapsed):
        event = None

        if elapsed == 6:
            event = "SMOKE_DETECTED_A"

        if elapsed >= 6:
            density_a = self.get_density("A")
            speed_a = self.get_speed(density_a)

            move = int(min(5, self.zones["A"]) * speed_a)

            self.zones["A"] -= move
            self.zones["B"] += int(move * 0.7)
            self.zones["C"] += int(move * 0.3)

        congestion_event = self.check_congestion("B")
        if congestion_event:
            event = congestion_event

            spill = 2
            self.zones["B"] = max(0, self.zones["B"] - spill)
            self.zones["C"] += spill
        
        if self.zones["A"] == 0:
            event = "ZONE_A_CLEARED"

        return event

    def blocked_exit_scenario(self):
        event = None

        if elapsed == 6:
            event = "EXIT_BLOCKED_B"

        if elapsed >= 6:
            density_b = self.get_density("B")
            speed_b = self.get_speed(density_b)

            move = int(min(5, self.zones["A"]) * speed_b)

            self.zones["A"] -= move
            self.zones["B"] += move  # ALL go into B (bottleneck)

        congestion_event = self.check_congestion("B")
        if congestion_event:
            event = congestion_event

        return event

    def false_alarm_scenario(self):
        event = None

        if elapsed == 6:
            event = "FALSE_ALARM"

        # minimal movement
        if elapsed >= 6:
            fluctuation = 1
            self.zones["A"] = max(0, self.zones["A"] + random.randint(-fluctuation, fluctuation))
            self.zones["B"] = max(0, self.zones["B"] + random.randint(-fluctuation, fluctuation))
            self.zones["C"] = max(0, self.zones["C"] + random.randint(-fluctuation, fluctuation))

        return event

    def step(self, current_time):
        if self.start_time is None:
            self.start_time = current_time

        self.time = current_time
        elapsed = (self.time - self.start_time).total_seconds()

        if self.scenario_type == "fire":
            event = self.fire_scenario(elapsed)
        
        elif self.scenario_type == "blocked_exit":
            event = self.blocked_exit_scenario(elapsed)

        elif self.scenario_type == "false_alarm":
            event = self.false_alarm_scenario(elapsed)

        else:
            raise ValueError("Unknown scenario type")

        return {
            "location_id": self.location_id,
            "scenario_id": self.scenario_id,
            "scenario_type": self.scenario_type,
            "time": self.time.isoformat(),
            "elapsed": elapsed,
            "zones": self.zones.copy(),
            "density": {z: round(self.get_density(z), 2) for z in self.zones},
            "speed": {z: round(self.get_speed(self.get_density(z)), 2) for z in self.zones},
            "event": event
        }