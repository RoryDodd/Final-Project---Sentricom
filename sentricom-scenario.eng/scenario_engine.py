import random
from datetime import datetime, timedelta

class ScenarioEngine:
    def __init__(self, scenario_type="fire"):
        self.scenario_id = f"{scenario_type}_scenario"
        self.scenario_type = scenario_type

        self.location_id = "East_Wing"

        self.start_time = None
        self.time = None

        self.raw_count = {
            "A": 50,
            "B": 30,
            "C": 20
        }

        self.zone_area = {
            "A": 50,
            "B": 40,
            "C": 30
        }

        self.prev_raw_counts = self.raw_count.copy()
        self.exit_blocked_triggered = False

        self.events = []

    def get_density(self, zone_id):
        return self.raw_count[zone_id] / self.zone_area[zone_id]

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

        if elapsed == 3:
            event = "SMOKE_DETECTED_A"

        if elapsed == 6:
            event = "FIRE_DETECTED_A"

        if elapsed == 9:
            event = "FIRE_ALARM_A_TRIGGERED"

        if elapsed >= 6:
            density_a = self.get_density("A")
            speed_a = self.get_speed(density_a)

            move = int(min(5, self.raw_count["A"]) * speed_a)

            self.raw_count["A"] -= move
            self.raw_count["B"] += int(move * 0.7)
            self.raw_count["C"] += int(move * 0.3)

        congestion_event = self.check_congestion("B")
        if congestion_event:
            event = congestion_event

            spill = 2
            self.raw_count["B"] = max(0, self.raw_count["B"] - spill)
            self.raw_count["C"] += spill
        
        if self.raw_count["A"] == 0:
            event = "ZONE_A_CLEARED"

        return event

    def blocked_exit_scenario(self, elapsed):
        event = None

        if elapsed == 3:
            event = "EVACUATION_STARTED"

        if elapsed >= 6:
            density_b = self.get_density("B")
            speed_b = self.get_speed(density_b)

            move = int(min(5, self.raw_count["A"]) * speed_b)

            self.raw_count["A"] -= move
            self.raw_count["B"] += move  # ALL go into B (bottleneck)
        
        if (
            not self.exit_blocked_triggered and
            self.raw_count["A"] < self.prev_raw_counts["A"] and
            self.raw_count["B"] > self.prev_raw_counts["B"] and
            self.get_density("B") > 2.5
        ):
            event = "EXIT_BLOCKED_B"
            self.exit_blocked_triggered = True

        congestion_event = self.check_congestion("B")
        if congestion_event and not event:
            event = congestion_event

        return event

    def false_alarm_scenario(self, elapsed):
        event = None

        if elapsed == 6:
            event = "FALSE_ALARM"

        # minimal movement
        if elapsed >= 6:
            fluctuation = 1
            self.raw_count["A"] = max(0, self.raw_count["A"] + random.randint(-fluctuation, fluctuation))
            self.raw_count["B"] = max(0, self.raw_count["B"] + random.randint(-fluctuation, fluctuation))
            self.raw_count["C"] = max(0, self.raw_count["C"] + random.randint(-fluctuation, fluctuation))

        return event

    def step(self, current_time):
        if self.start_time is None:
            self.start_time = current_time

        self.time = current_time
        elapsed = int((self.time - self.start_time).total_seconds())

        if self.scenario_type == "fire":
            event = self.fire_scenario(elapsed)
        
        elif self.scenario_type == "blocked_exit":
            event = self.blocked_exit_scenario(elapsed)

        elif self.scenario_type == "false_alarm":
            event = self.false_alarm_scenario(elapsed)

        else:
            raise ValueError("Unknown scenario type")

        self.prev_raw_counts = self.raw_count.copy()

        return {
            "location_id": self.location_id,
            "scenario_id": self.scenario_id,
            "scenario_type": self.scenario_type,
            "time": self.time.isoformat(),
            "elapsed": elapsed,
            "raw_counts": self.raw_count.copy(),
            #"density": {z: round(self.get_density(z), 2) for z in self.raw_count},
            "speed": {z: round(self.get_speed(self.get_density(z)), 2) for z in self.raw_count},
            "event": event
        }