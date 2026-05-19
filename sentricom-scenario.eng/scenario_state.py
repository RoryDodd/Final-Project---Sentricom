#scenario_state.py

# Had to move state messge definitions to shared class as used by two parts of application

# ---------------------------------------------------------------------------
# Health Output Message Model
# ---------------------------------------------------------------------------


from datetime import datetime, timezone

STATE = {
    "status": "starting",
    "last_message": "Scenario simulator starting",
    "last_seen_at" : None,
    "active_scenario": "None",
    "Event": "None",
    "steps_requested": 0,
    "steps_completed": 0,
    "zones_generated": 0,
    "summary_status": None,
    
}

def set_state(status, message=None):
    STATE["status"] = status
    STATE["last_seen_at"] = datetime.now(timezone.utc).isoformat()
    if message:
        STATE["last_message"] = message