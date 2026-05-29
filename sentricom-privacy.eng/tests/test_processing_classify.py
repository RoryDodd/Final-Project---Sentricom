__author__ = "R Dodd"
__version__ = "1.0"
__date__ = "May 2026"

"""This test file checks that classify() returns the right risk level and that process_through_dp() produces a valid processed record with the expected fields.
"""

import sys
from pathlib import Path

# Ensure the dp_engine module can be imported from the parent directory
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import the functions to test from dp_engine (must import after adjusting sys.path)
from dp_engine import classify, process_through_dp

# Example minimal config
DP_CONFIG = {"mechanism": "discrete_laplace", "epsilon": 0.4}

# A low count with low risk should be classified as SAFE
def test_classify_safe():
    risk = classify(10, 1.0)
    assert risk == "SAFE"

# A moderate count should be classified as MONITOR
def test_classify_monitor():
    risk = classify(20, 1.0)
    assert risk == "MONITOR"

# A high count with high risk should be classified as EVACUATE
def test_classify_evacuate():
    risk = classify(30, 3.0)
    assert risk == "EVACUATE"


def test_process_through_dp_length():
    # Example input record that simulates one zone coming through the DP pipeline
    fake_data = [
        {
            "zone_id": "1",
            "zone_name": "Main Lobby",
            "real_count": 15,
            "timestamp": "2026-05-22T12:00:00Z",
        }
    ]
    # Run the data through the differential privacy processing function
    results = process_through_dp(fake_data, dp_config=DP_CONFIG)
    assert len(results) == 1 # The function should return one processed record
    # Check that the expected output fields exist and have the right type
    dp = results[0]
    assert "dp_count" in dp
    assert "risk_level" in dp
    assert isinstance(dp["dp_count"], int)