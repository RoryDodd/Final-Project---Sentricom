#scenario_server.py

import json
import os
import settings

from http.server import BaseHTTPReuestHandler, ThreadingHTTPServer
from scenario_client import run_scenario

# ---------------------------------------------------------------------------
# Health Output Message Model
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# Request Handler
# ---------------------------------------------------------------------------

class SimulatorHandler(BaseHTTPRequestHandler):
    # Healthcheck get endpoint
    def do_GET(self):
        if self.path != "/health":
            self.send_response(404)
            self.end_headers()
            return
            
        body = json.dumps({
            "ok": True,
            "service": settings.SERVICE_NAME,
            "service_version": settings.SERVICE_VERSION,
            **STATE,
        }).encode("utf-8")
            
            
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        
    # Zones Post endpoint - kicks off simulator run
    def do_POST(self):
        if self.path != "/run":
            self.send_response(404)
            self.end_headers()
            return
                   
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            
        try:
            data = json.loads(raw_body)
            
            scenario = data.get("scenario") or os.getenv("DEFAULT_SCENARIO", "fire")
            steps = int(data.get("steps", os.getenv("DEFAULT_STEPS", "25")))
            delay = float(data.get("delay", os.getenv("DEFAULT_DELAY", "1")))
            
            # Run Scenario Simulator
            result = run_scenario(scenario_type=scenario, steps=steps, delay=delay)
            
            response = json.dumps(result).encode("utf-8")
            self.send_response(200)
            
        except Exception as e:
            set_state("error", f"Scenario run failed: {e}")
            response = json.dumps({
                "ok": False,
                "error": str(e)
            }).encode("utf-8")
            self.send_response(500)
            
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)
        
    def log_message(self, format, *args):
        return

     
def main():
    host = os.getenv("HEALTH_HOST",  os.getenv("HOST", "0.0.0.0"))
    port = int(os.getenv("PORT", os.getenv("HEALTH_PORT", "8040")))
    
    set_state("idle", "Scenario simulator ready")
    
    server = ThreadingHTTPServer((host, port), SimulatorHandler)
    print(f"Scenario Sim Service runnin on http://{host}:{port}")
    print(f"Health Check: http://{host}:{port}/health")
    print(f"Run Endpoint: http://{host}:{port}/run")
    server.serve_forever()

    

if __name__ == "__main__":
    main()
    