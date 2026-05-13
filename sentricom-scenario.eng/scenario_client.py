import requests
import time
from scenario_engine import ScenarioEngine
from datetime import datetime, timedelta

API_URL = "https://afert-umber.vercel.app/occupancy/testdata"
API_KEY = "2a92652f69031a93302e5ec20f0758a9f364e7206b300fa027118f2d71a1e7aa"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

dp_config = {
    "mechanism": "discrete_laplace",
    "epsilon": 0.7,
    "delta": 1e-5
}

scenarios = ["fire",
    #"blocked_exit",
    #"false_alarm"
]

# ADDED: mapping from engine zones → API names
ZONE_MAP = {
    "A": "Main Lobby",
    "B": "Corridor B",
    "C": "Auditorium",
    "D": "EXIT_SOUTH",
    "E": "Offices_South",
    "F": "Offices_East"
}

def main():
    start_time = datetime.now()

    for scenario_type in scenarios:
        scenario = ScenarioEngine(scenario_type=scenario_type)

        print(f"--- Starting scenario: {scenario_type} ---")

        for i in range(25):
            current_time = start_time + timedelta(seconds=3 * i)

            state =scenario.step(current_time)

            timestamp = datetime.now().isoformat() + "Z"

            # Used to package the zones up into the format expected by the API
            zones_payload = []
            zone_id = 1

            for zone_key, count in state["raw_counts"].items():

                zones_payload.append({
                    "timestamp": timestamp,
                    "zone_id": zone_id,
                    "zone_name": ZONE_MAP.get(zone_key, zone_key),
                    "real_count": count,
                    "risk_status": "LOW RISK",
                    "event": state["event"],
                    "vuln_flag": (
                        state["vulnerable_flag"].get(zone_key)
                        if state["vulnerable_flag"].get(zone_key) is True
                        else False
                    ),
                })

                zone_id += 1

            try:
                res = requests.put(API_URL, json=zones_payload, headers=headers)
                response_data = res.json()
            except Exception as e:
                response_data = {"error": str(e)}

            print("Sent:", zones_payload)
            print("Response:", response_data)
            print("-" * 50)

            time.sleep(1)

if __name__ == "__main__":
    main()