import requests
import time
import sys
import os
from datetime import datetime
from dp_engine import create_dp, classify

# External API to retrieve test data
EXTERNAL_API_URL = "https://afert-umber.vercel.app/occupancy/testdata/next"
API_KEY = "2a92652f69031a93302e5ec20f0758a9f364e7206b300fa027118f2d71a1e7aa"

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

# Default DP config
DEFAULT_DP_CONFIG = {
    "mechanism": "discrete_laplace",
    "epsilon": 0.7,
    "delta": 1e-5
}


def fetch_next_data():
    """Fetch next line of test data from the external API."""
    try:
        res = requests.get(EXTERNAL_API_URL, headers=headers)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 204:  # No more data
            return None
        print(f"Error fetching from external API: {e}")
        return None
    except Exception as e:
        print(f"Error fetching from external API: {e}")
        return None


def process_through_dp(zone_data, dp_config=None):
    """
    Process zone data through differential privacy engine.
    
    Input: zone_data from external API
    [
        {
            "timestamp": "...",
            "zone_id": 1,
            "zone_name": "Main Lobby",
            "real_count": 50,
            "risk_status": "...",
            "event": "...",
            "vuln_flag": False
        },
        ...
    ]
    
    Output: DP-protected version with noise added
    """
    if not dp_config:
        dp_config = DEFAULT_DP_CONFIG
    
    # Create DP mechanism
    dp = create_dp(dp_config)
    
    results = []
    
    for zone in zone_data:
        real_count = zone.get("real_count", 0)
        zone_name = zone.get("zone_name", "Unknown")
        
        # Map zone name to zone letter for area lookup
        zone_map = {
            "Main Lobby": "A",
            "Corridor B": "B",
            "Exit Hall": "C"
        }
        zone_key = zone_map.get(zone_name, "A")
        zone_area = ZONE_AREAS.get(zone_key, 50)
        
        # Apply DP noise
        dp_count = dp.privatize_count(real_count)
        
        # Recalculate density using DP count
        dp_density = dp_count / zone_area
        
        # Classify risk
        risk_level = classify(dp_count, dp_density)
        
        # Create result
        dp_zone = {
            "timestamp": zone.get("timestamp"),
            "zone_id": zone.get("zone_id"),
            "zone_name": zone_name,
            "real_count": real_count,
            "dp_count": dp_count,
            "dp_density": round(dp_density, 2),
            "risk_level": risk_level,
            "epsilon": dp.epsilon,
            "mechanism": dp_config.get("mechanism", "discrete_laplace"),
            "event": zone.get("event"),
            "vuln_flag": zone.get("vuln_flag", False)
        }
        
        results.append(dp_zone)
    
    return results


def display_results(original_data, dp_results):
    """Pretty print original vs DP-protected data."""
    print("\n" + "=" * 80)
    print("DIFFERENTIAL PRIVACY PROCESSING")
    print("=" * 80)
    
    for i, (orig, dp) in enumerate(zip(original_data, dp_results)):
        # Format timestamp
        timestamp_str = orig.get('timestamp', '')
        try:
            ts = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            formatted_ts = ts.strftime("%d/%m/%Y - %H:%M:%S")
        except:
            formatted_ts = timestamp_str
        
        print(f"\nZone {i+1}: {orig.get('zone_name', 'Unknown')}")
        print(f"  Timestamp: {formatted_ts}")
        print(f"  Real Count: {orig.get('real_count')} → DP Count: {dp['dp_count']} (ε={dp['epsilon']})")
        print(f"  Density: {orig.get('real_count')}/{ZONE_AREAS.get('A')} → {dp['dp_density']}")
        print(f"  Risk: {dp['risk_level']}")
        print(f"  Event: {orig.get('event', 'None')}")
        print(f"  Vulnerable: {orig.get('vuln_flag', False)}")
    
    print("\n" + "=" * 80)


def main():
    print("Privacy Engine - Fetching test data and applying differential privacy")
    print(f"Data Source: {EXTERNAL_API_URL}")
    print("-" * 80)
    
    batch_count = 0
    total_zones_processed = 0
    
    while True:
        # Fetch next batch of data
        response = fetch_next_data()
        
        if not response:
            print("\nNo more data available.")
            break
        
        batch_count += 1
        
        # Extract zones from the response
        zones = response.get("zones", [])
        print(f"\n[Batch {batch_count}] Received {len(zones)} zones (batch_id: {response.get('batch_id')})")
        
        if not zones:
            print("No zones in response, stopping.")
            break
        
        # Process through DP
        dp_results = process_through_dp(zones, DEFAULT_DP_CONFIG)
        total_zones_processed += len(dp_results)
        
        # Display results
        display_results(zones, dp_results)
        
        # Wait before fetching next batch
        time.sleep(0.5)
    
    print(f"\n✓ Processing complete. Total zones processed: {total_zones_processed}")


if __name__ == "__main__":
    main()
