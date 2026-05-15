import json
import os
import threading
import settings
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ---------------------------------------------------------------------------
# Output Message Model
# ---------------------------------------------------------------------------

STATE = {
    "status": "starting",
    "last_message": "Privacy engine starting",
    "last_seen_at" : None,
    "batches_processed": 0,
    "zones_processed": 0,
}

def set_state(status, message=None):
    STATE["status"] = status
    STATE["last_seen_at"] = datetime.now(timezone.utc).isoformat()
    if message:
        STATE["last_message"] = message
        
# ---------------------------------------------------------------------------
# Request Handler
# ---------------------------------------------------------------------------
class HealthHandler(BaseHTTPRequestHandler):
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
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        
    def log_message(self, format, *args):
        return
        
# ---------------------------------------------------------------------------
# Run Controls
# ---------------------------------------------------------------------------
def start_health_server():
    host = os.getenv("HEALTH_HOST", "::")
    port = int(os.getenv("HEALTH_PORT", "8032"))
    
    server = ThreadingHTTPServer((host, port), HealthHandler)
    server.serve_forever()
    
def start_health_thread():
    thread = threading.Thread(target=start_health_server, daemon=True)
    thread.start()