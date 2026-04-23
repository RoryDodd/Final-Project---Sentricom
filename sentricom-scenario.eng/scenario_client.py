import requests
import time
from scenario_engine import ScenarioEngine
from datetime import datetime, timedelta

API_URL = "https://afert-umber.vercel.app/api/v1/zones/latest"

def main():
    scenarios = ["fire", "blocked_exit", "false_alarm"]
    start_time = datetime.now()

    for scenario_type in scenarios:
        scenario = ScenarioEngine(scenario_type=scenario_type)

        for i in range(10):
            current_time = start_time + timedelta(seconds=3 * i)

            state =scenario.step(current_time)

            payload = {
                "location_id": state["location_id"],
                "scenario_id": state["scenario_id"],
                "scenario_type": state["scenario_type"],
                "timestamp": state["time"],
                "zones": state["zones"],
                "time_elapsed": state["elapsed"],
                "density": state["density"],  
                "speed": state["speed"],
                "event": state["event"]
            }

            res = requests.put(API_URL, json=payload)

            print("Sent:", payload)
            print("Response:", res.json())
            print("-" * 50)

            time.sleep(1)

if __name__ == "__main__":
    main()