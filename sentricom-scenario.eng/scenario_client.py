#scenario_client.py

import os
import time
import requests
from scenario_engine import ScenarioEngine
from scenario_state import set_state, STATE
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
RAW_TEST_SUMMARY_URL = os.getenv("RAW_TEST_SUMMARY_URL")

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# SHOULDN'T BE REQUIRED HERE NOW
'''
dp_config = {
    "mechanism": "discrete_laplace",
    "epsilon": 0.7,
    "delta": 1e-5
}

scenarios = ["fire",
    #"blocked_exit",
    #"false_alarm"
]
'''

# ADDED: mapping from engine zones → API names
ZONE_MAP = {
    "A": "Main Lobby",
    "B": "Corridor B",
    "C": "Auditorium",
    "D": "EXIT_SOUTH",
    "E": "Offices_South",
    "F": "Offices_East"
}

# Raw test data send point if required
def send_raw_test_summary(summary_payload):
    if not RAW_TEST_SUMMARY_URL:
        STATE["summary_status"] = "skipped"
        set_state("summary_skipped", "RAW_TEST_SUMMARY_URL not configured")
        return {
            "ok": False,
            "status": "skipped",
            "message": "RAW_TEST_SUMMARY_URL not configured",
        }
        
    try:
        set_state("sending_summary", "Attempting to send run summary report")
        STATE["summary_status"] = "sending"
        
        response = requests.post(
            RAW_TEST_SUMMARY_URL,
            json=summary_payload,
            headers=headers,
            timeout=10
        )
        
        if response.ok:
            STATE["summary_status"] = "sent"
            set_state("summary_sent", "Run summary status report sent")
            return {
                "ok": True,
                "status_code": response.status_code,
                "response":  response.json() if response.text else None,
            }
            
        STATE ["summary_status"] = "failed"
        set_state("summary_failed", f"Run summary report sending failed: {response.status_code}")
        return {
            "ok": False,
            "status_code": response.status_code,
            "response": response.text,
        }
        
    except Exception as e:
        STATE["summary_status"] = "failed"
        set_state("summary_failed", f"Rim summary report sending failed: {e}")
        return {
            "ok": False,
            "error": str(e),
        }

def run_scenario(scenario_type="fire", steps=25, delay=1):
    scenario_type = scenario_type or os.getenv("DEFAULT_SCENARIO", "fire")
    
    # Initiate Scenario Run
    start_time = datetime.now()
    run_id = f"{scenario_type}_{start_time.strftime('%Y%m%d_%H%M%S')}"
    
    scenario = ScenarioEngine(scenario_type=scenario_type)
    
    STATE["active_scenario"] = scenario_type
    STATE["steps_requested"] = steps
    STATE["steps_completed"] = 0
    STATE["zones_generated"] = 0
    STATE["summary_status"] = None
    
    set_state("running", f"Scenario run initialised with type {scenario_type}")
    print(f"--- Starting scenario: {scenario_type} ---")
    
    # Export block if needed
    run_summary = {
        "run_id": run_id,
        "scenario": scenario_type,
        "started_at": start_time.isoformat(),
        "steps_requested": steps,
        "zone_runs": [],
    }
    
    for i in range(steps):
            current_time = start_time + timedelta(seconds=3 * i)
            state =scenario.step(current_time)

            timestamp = datetime.now().isoformat() + "Z"

            # Used to package the zones up into the format expected by the API
            zones_payload = []
            zone_id = 1
            
            STATE["event"] = state.get("event")
            set_state("generating", f"Generating step {i + 1} of {steps}")
            
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
                
            # Update the export array
            run_summary["zone_runs"].append({
                "step": i + 1,
                "timestamp": timestamp,
                "event": state.get("event"),
                "zones": zones_payload,
            })

            # Try catch with inner error exception handling
            try:
                set_state("sending", f"Sending step {i + 1} of {steps}")
                response = requests.put(API_URL, json=zones_payload, headers=headers, timeout=10)
            
                try:
                    response_data = res.json()
                except Exception as e:
                    response_data = response.text
                    
            except Exception as e:
                response_data = {"error": str(e)}
                
            STATE["steps_completed"] += 1
            STATE["zones_generated"] += len(zones_payload)

            print("Sent:", zones_payload)
            print("Response:", response_data)
            print("-" * 50)

            time.sleep(delay)
            
    finished_at = datetime.now().isoformat()

    run_summary["finished_at"] = finished_at
    run_summary["steps_completed"] = STATE["steps_completed"]
    run_summary["zones_generated"] = STATE["zones_generated"]
    
    summary_result = send_raw_test_summary(run_summary)
    set_state("idle", f"Scenario {scenario_type} completed")
            
    return {
        "ok": True,
        "run_id": run_id,
        "scenario": scenario_type,
        "steps_requested": steps,
        "steps_completed": STATE["steps_completed"],
        "zones_generated": STATE["zones_generated"],
        "summary_result": summary_result,    
    }

# Now called externally but can also be called locally - main loop just calls above function
def main():
    # Define these values for local run in .env file in application root
    def main():
        run_scenario(
            scenario_type=os.getenv("DEFAULT_SCENARIO", "fire"),
            steps=int(os.getenv("DEFAULT_STEPS", "25")),
            delay=float(os.getenv("DEFAULT_DELAY", "1")),
        )

if __name__ == "__main__":
    main()