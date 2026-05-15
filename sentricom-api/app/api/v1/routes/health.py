# app/api/v1/routes/health.py

import os
import requests
from fastapi import APIRouter, Depends
from app.dependencies.auth_dep import require_api_key
from pathlib import Path

router = APIRouter()

# Keep warm
@router.get("/remote-hello", tags=["Health"])
def remote_hello():
    return {"ok": True, "message": "Hello from Sentricom API!"}


# Returns environmeant health
@router.get("/health", tags=["Health"])
def health_check(auth=Depends(require_api_key)):
    """
    Health check endpoint to verify that the API is running.
    """
    checks = {}

    # 1. Folder stucture check
    required_dirs = [
        "app/api",
        "app/models",
        "app/schemas",
        "app/services",
        "app/db",
        "tmp/db",
    ]

    for d in required_dirs:
        checks[d] = Path(d).exists() and Path(d).is_dir()

    # 2. Check config file present
    checks["config_present"] = Path("app/core/config.py").exists()

    # 3. Check Privacy Engine running (if configured)

    # Privacy Engine URI address
    privacy_health_url = os.getenv("PRIVACY_ENGINE_HEALTH_URL")

    if privacy_health_url:
        try:
            response = requests.get(privacy_health_url, timeout=4)
            checks["privacy_engine_reachable"] = response.status_code == 200
            checks["privacy_engine"] = response.json()
        except Exception as e:
            checks["privacy_engine_reachable"] = False
            checks["privacy_engine_error"] = str(e)

    else:
        checks["privacy_engine_reachable"] = False
        checks["privacy_engine_error"] = "PRIVACY_ENGINE_HEALTH_URL not configured"
    
    # 4. Final status - all checks passed
    #all_ok = all(checks.values())
    all_ok = (
        all(checks[d] for d in required_dirs)
        and checks["config_present"]
        and checks.get("privacy_engine_reachable", False) 
    )

    return {
        "status": "Sentricom API health checks passed" if all_ok else "health check failures",
        "check_results": checks
    }


