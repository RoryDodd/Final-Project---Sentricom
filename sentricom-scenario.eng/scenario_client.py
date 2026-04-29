import requests
import time
from scenario_engine import ScenarioEngine
from datetime import datetime, timedelta

API_URL = "https://afert-umber.vercel.app/api/v1/zones/latest"

dp_config = {
    "mechanism": "discrete_laplace",
    "epsilon": 0.7,
    "delta": 1e-5
}

scenarios = ["fire", "blocked_exit", "false_alarm"]

def main():
    start_time = datetime.now()

    for scenario_type in scenarios:
        scenario = ScenarioEngine(scenario_type=scenario_type)

        print(f"--- Starting scenario: {scenario_type} ---")

        for i in range(10):
            current_time = start_time + timedelta(seconds=3 * i)

            state =scenario.step(current_time)

            payload = {
                "location_id": state["location_id"],
                "scenario_id": state["scenario_id"],
                "scenario_type": state["scenario_type"],
                "time": state["time"],
                "raw_counts": state["raw_counts"],
                "time_elapsed": state["elapsed"],
                "speed": state["speed"],
                "event": state["event"],
                "dp_config": dp_config
            }
            try:
                res = requests.put(API_URL, json=payload)
                response_data = res.json()
            except Exception as e:
                response_data = {"error": str(e)}

            print("Sent:", payload)
            print("Response:", response_data)
            print("-" * 50)

            time.sleep(1)

if __name__ == "__main__":
    main()