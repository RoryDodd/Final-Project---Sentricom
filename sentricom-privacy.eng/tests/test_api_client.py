__author__ = "R Dodd"
__version__ = "1.0"
__date__ = "May 2026"

"""This file checks that the client can fetch the next batch of test data, handle the no-data case and successfully post DP-processed results.
"""

import os
import sys
from pathlib import Path
from unittest.mock import patch

# Ensure the dp_engine module can be imported from the parent directory
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Test environment values used to mock the API configuration
ENV = {
    "EXTERNAL_API_URL_BASE": "https://afert-staging.up.railway.app/occupancy/testdata",
    "API_KEY": "2a92652f69031a93302e5ec20f0758a9f364e7206b300fa027118f2d71a1e7aa",
}

@patch.dict(os.environ, ENV, clear=False)
@patch("requests.get")
def test_fetch_next_data_ok(mock_get):
    from api import fetch_next_data
    mock_get.return_value.status_code = 200 # Simulate a successful API response
    mock_get.return_value.json.return_value = {"zones": [], "batch_id": "test_batch"}
    # The function should return the JSON payload from the API
    assert fetch_next_data() == {"zones": [], "batch_id": "test_batch"}

@patch.dict(os.environ, ENV, clear=False)
@patch("requests.get")
def test_fetch_next_data_no_data(mock_get):
    from api import fetch_next_data
    mock_get.return_value.status_code = 204 # Simulate a No Content response
    # The function should return None when there is no data available
    assert fetch_next_data() is None

@patch.dict(os.environ, ENV, clear=False)
@patch("requests.put")
def test_post_dp_results_success(mock_put):
    from api import post_dp_results
    mock_put.return_value.status_code = 200 # Simulate a successful PUT request
    mock_put.return_value.json.return_value = {"ok": True}
    # Example DP result record in the format expected by the API client
    result = post_dp_results("batch_1", [{
        "zone_id": 1,
        "zone_name": "Main Lobby",
        "timestamp": "2026-05-22T12:00:00Z",
        "dp_count": 10,
        "risk_level": "SAFE",
    }])
    # The function should return the API response JSON
    assert result == {"ok": True}