__author__ = "R Dodd"
__version__ = "1.0"
__date__ = "May 2026"

"""This file checks that the service name is correct and that the version is stored as a string.
"""
import sys
from pathlib import Path

# Ensure the dp_engine module can be imported from the parent directory
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from settings import SERVICE_NAME, SERVICE_VERSION

# Test that the service metadata constants are defined and have the expected values
def test_service_metadata():
    assert SERVICE_NAME == "Sentricom Privacy Engine"
    assert isinstance(SERVICE_VERSION, str)