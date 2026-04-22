from fastapi import APIRouter
from pathlib import Path

router = APIRouter()

@router.get("/health", tags=["Health"])
def health_check():
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
        "app/db"
    ]

    for d in required_dirs:
        checks[d] = Path(d).exists() and Path(d).is_dir()

    # 2. Check config file present
    checks["config_present"] = Path("app/core/config.py").exists()
    
    # 4. Final status - all checks passed
    all_ok = all(checks.values())

    return {
        "status": "Sentricom API health checks passed" if all_ok else "health check failures",
        "check_results": checks
    }


