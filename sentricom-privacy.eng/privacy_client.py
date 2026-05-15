__author__ = "R Dodd", "Richard Avery", "L Gardiner"
__version__ = "2.0"
__date__ = "2026"

from health_server import start_health_thread, set_state, STATE
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import time
import api
import dp_engine as dp
import os


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

def display_results(original_data, dp_results):
    """Pretty print original vs DP-protected data."""
    print("\n" + "=" * 80)
    print("DIFFERENTIAL PRIVACY PROCESSING")
    print("=" * 80)

    for i, (orig, dp) in enumerate(zip(original_data, dp_results)):
        timestamp_str = orig.get('timestamp', '')
        try:
            ts = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            formatted_ts = ts.strftime("%d/%m/%Y - %H:%M:%S")
        except:
            formatted_ts = timestamp_str

        print(f"\nZone {i+1}: {orig.get('zone_name', 'Unknown')}")
        print(f"  Timestamp:  {formatted_ts}")
        print(f"  Real Count: {orig.get('real_count')} → DP Count: {dp['dp_count']} (ε={dp['epsilon']})")
        print(f"  Density:    {orig.get('real_count')}/{api.ZONE_AREAS.get('A')} → {dp['dp_density']}")
        print(f"  Risk:       {dp['risk_level']}")
        print(f"  Event:      {orig.get('event', 'None')}")
        print(f"  Vulnerable: {orig.get('vuln_flag', False)}")

    print("\n" + "=" * 80)

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main():
    # Start health check for external app snapshot
    start_health_thread()
    set_state("running", "Privacy engine loop started")
    
    host = os.getenv("HEALTH_HOST", "localhost")
    port = os.getenv("HEALTH_PORT", "8034")
    
    display_host = "localhost" if host in ["0.0.0.0"] else host
    # Start-Up Confirmation
    print("Privacy Engine - Fetching test data and applying differential privacy")
    print(f"Initialising Health-Check at: http://{display_host}:{port}/health")
    print(f"Data Source:  {api.EXTERNAL_API_URL + api.RETRIEVE_ENDPOINT}")
    print(f"Ingest API:   {api.EXTERNAL_API_URL + api.POST_ENDPOINT}")
    print("-" * 80)

    batch_count = 0
    total_zones_processed = 0

    while True:
        # Fetch next batch
        response = api.fetch_next_data()

        if not response:
            # Health-check update
            set_state("waiting", "Waiting for more data to be available")
            # Console update
            print("\nWaiting for more data to be available.")
            time.sleep(5)
            continue

        batch_count += 1
        batch_id = response.get("batch_id", f"batch_{batch_count}")
        zones = response.get("zones", [])
        # Health-Check update
        set_state("processing", f"Processing batch {batch_id}")
        # Console update
        print(f"\n[Batch {batch_count}] Received {len(zones)} zones (batch_id: {batch_id})")

        if not zones:
            print("No zones in response, stopping.")
            break

        # Process through DP
        dp_results = dp.process_through_dp(zones, api.DEFAULT_DP_CONFIG)
        total_zones_processed += len(dp_results)

        # Display results in terminal (debug)
        display_results(zones, dp_results)

        # POST results to Vercel backend
        api.post_dp_results(batch_id, dp_results)
        
        # Health-Check tracking
        STATE["batches_processed"] += 1
        STATE["zones_processed"] += len(dp_results)
        set_state("idle", f"Processed batch {batch_id}")

        # Wait before fetching next batch
        time.sleep(1.5)

    print(f"\n✓ Processing complete. Total zones processed: {total_zones_processed}")


if __name__ == "__main__":
    main()