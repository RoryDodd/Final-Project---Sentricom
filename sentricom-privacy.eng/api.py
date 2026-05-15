__author__ = "R Dodd, L Gardiner"
__version__ = "2.1"
__date__ = "2026"

import requests
import os
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# Load API endpoint base from file
load_dotenv()

# External API Base and Endpoint to retrieve test data
# (Simulates data from sensor nodes)
#EXTERNAL_API_URL = "https://afert-umber.vercel.app/occupancy/testdata/next"
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL_BASE")
RETRIEVE_ENDPOINT = "/occupancy/testdata/next"

# API Base and Endpoint to POST DP-processed results to
#INGEST_API_URL = "https://afert-umber.vercel.app/api/v1/zones/latest"
#INGEST_API_URL = os.getenv("INGEST_API_URL_BASE")
POST_ENDPOINT = "/api/v1/zones/latest"

#API_KEY = "2a92652f69031a93302e5ec20f0758a9f364e7206b300fa027118f2d71a1e7aa"
API_KEY = os.getenv("API_KEY")

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Zone areas for density calculation
ZONE_AREAS = {
    "A": 50,
    "B": 40,
    "C": 30
}

# Zone capacities matching the DB
ZONE_CAPACITIES = {
    1: 100,  # Main Lobby
    2: 75,   # Level 1 - North Wing
    3: 75,   # Level 1 - South Wing
}

# Default DP config
DEFAULT_DP_CONFIG = {
    "mechanism": "discrete_laplace",
    "epsilon": 0.7,
    "delta": 1e-5
}

# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

def fetch_next_data():
    """Fetch next batch of test data from the external API."""
    try:
        res = requests.get(EXTERNAL_API_URL + RETRIEVE_ENDPOINT, headers=headers, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 204:  # No more data
            return None
        print(f"No data available from external API: {e}")
        return None
    except Exception as e:
        print(f"Error fetching from external API: {e}")
        return None
    
# ---------------------------------------------------------------------------
# POST to Vercel backend
# ---------------------------------------------------------------------------

def post_dp_results(batch_id, dp_results):
    """PUT DP-processed batch results to the Vercel zones endpoint."""

    # Map dp_results fields to ZoneLatest schema
    payload = [
    {
        "zone_id": r["zone_id"],
        "zone_name": r["zone_name"],
        "time": r["timestamp"],
        "dp_count": int(r["dp_count"]),
        "risk_level": r["risk_level"],
        "vuln_flag": r.get("vuln_flag", False),
        "capacity": ZONE_CAPACITIES.get(r["zone_id"], 100),
        "risk_status": r["risk_level"].lower(),
        "site_id": 1,
    }
    for r in dp_results
]

    try:
        res = requests.put(EXTERNAL_API_URL + POST_ENDPOINT, json=payload, headers=headers, timeout=10)
        res.raise_for_status()
        print(f"  ✓ Sent batch {batch_id} ({len(payload)} zones) → {res.status_code} {res.json()}")
        return res.json()
    except requests.exceptions.HTTPError as e:
        print(f"  ✗ Failed to send batch {batch_id}: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        print(f"  ✗ Failed to send batch {batch_id}: {e}")
        return None