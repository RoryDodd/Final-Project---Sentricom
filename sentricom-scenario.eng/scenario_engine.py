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
            "C": 20,
            "D": 27,
            "E": 15,
            "F": 23
        }

        self.zone_area = {
            "A": 50,
            "B": 40,
            "C": 30,
            "D": 35,
            "E": 25,
            "F": 45
        }

        self.zones = list(self.raw_count.keys())

        self.evacuation_routes = {
            "A": "B",
            "B": "C",
            "C": "D",
            "D": "EXIT",
            "E": "D",
            "F": "E"
        }

        self.prev_raw_counts = self.raw_count.copy()

        self.exit_blocked_triggered = False

        self.active_vulnerable_zone = random.choice(self.zones)
        self.last_vulnerable_switch = 0

        self.events = []

    #Density Model: People per square meter, calculated from raw count and zone area.
    def get_density(self, zone_id):
        return self.raw_count[zone_id] / self.zone_area[zone_id]

    # Speed Model: Based on the fire engineering crowd flow model
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
        
        return None

    def update_vulnerability_focus(self, elapsed):
        # switch every 3–6 seconds (controls rotation speed)
        if elapsed - self.last_vulnerable_switch >= random.randint(3, 6):

            if self.active_vulnerable_zone is None:

                if random.random() < 0.1:
                    self.active_vulnerable_zone = random.choice(self.zones)

            else:
                current_index = self.zones.index(self.active_vulnerable_zone)

                if current_index < len(self.zones) - 1:
                    self.active_vulnerable_zone = self.zones[current_index + 1]

                else:
                    self.active_vulnerable_zone = None

            self.last_vulnerable_switch = elapsed

    def get_vulnerable_flags(self):
        if self.active_vulnerable_zone is None:
            return {zone: False for zone in self.zones}
        return {
            zone: zone == self.active_vulnerable_zone
            for zone in self.zones
        }

    def move_people(self, from_zone, to_zone):

        if to_zone == "EXIT":
            max_flow = 10
        else:
            max_flow = 7

        density = self.get_density(from_zone)
        speed = self.get_speed(density)

        available = self.raw_count[from_zone]

        move = int(min(max_flow, available) * speed)

        if move <= 0:
            return

        self.raw_count[from_zone] -= move
        if to_zone != "EXIT":
            self.raw_count[to_zone] += move

    def fire_scenario(self, elapsed):
        event = None

        if elapsed == 3:
            event = "SMOKE_DETECTED_A"

        if elapsed == 6:
            event = "FIRE_DETECTED_A"

        if elapsed == 9:
            event = "FIRE_ALARM_A_TRIGGERED"

        if elapsed >= 9:
            
            for from_zone, to_zone in self.evacuation_routes.items():
                self.move_people(from_zone, to_zone)

        return event

    def blocked_exit_scenario(self, elapsed):

        event = None

        if elapsed == 3:
            event = "EVACUATION_STARTED"

        if elapsed >= 6:
            
            self.evacuation_routes["B"] = "A"  # Redirect B back to A, simulating blocked exit
        
        for from_zone, to_zone in self.evacuation_routes.items():
            self.move_people(from_zone, to_zone)

        if (
            not self.exit_blocked_triggered and
            self.get_density("B") > 2.5
        ):
            event = "EXIT_BLOCKED_B"
            self.exit_blocked_triggered = True

        return event

    def false_alarm_scenario(self, elapsed):
        event = None

        if elapsed == 6:
            event = "FALSE_ALARM"

        # minimal movement
        if elapsed >= 6:
            for zone in self.zones:
                fluctuation = random.randint(-1, 1)

                self.raw_count[zone] = max(0, self.raw_count[zone] + fluctuation)

        return event

    def step(self, current_time):
        if self.start_time is None:
            self.start_time = current_time

        self.time = current_time
        elapsed = int((self.time - self.start_time).total_seconds())

        self.update_vulnerability_focus(elapsed)

        if self.scenario_type == "fire":
            event = self.fire_scenario(elapsed)
        elif self.scenario_type == "blocked_exit":
            event = self.blocked_exit_scenario(elapsed)
        elif self.scenario_type == "false_alarm":
            event = self.false_alarm_scenario(elapsed)
        else:
            raise ValueError("Unknown scenario type")

        self.prev_raw_counts = self.raw_count.copy()

        flags = self.get_vulnerable_flags()

        self.vulnerable_event = None

        for zone, active in flags.items():
            if active:
                self.vulnerable_event = (f"VULNERABLE_PERSONS_IDENTIFIED_{zone}")

        congestion_events = []

        for zone in self.zones:
            congestion = self.check_congestion(zone)
            if congestion:
                congestion_events.append(congestion)

        return {
            "location_id": self.location_id,
            "scenario_id": self.scenario_id,
            "scenario_type": self.scenario_type,
            "time": self.time.isoformat(),
            "elapsed": elapsed,
            "raw_counts": self.raw_count.copy(),
            "event": event,
            "vulnerable_event": self.vulnerable_event,
            "vulnerable_flag": self.get_vulnerable_flags(),
            "congestion_events": congestion_events
        }