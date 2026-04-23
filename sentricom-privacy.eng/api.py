from flask import Flask, request, jsonify
import requests
import dp_engine

app = Flask(__name__)

# Your teammate's API endpoint (replace this)
EXTERNAL_API_URL = "http://external-service/api/events"

# Choose DP mechanism
dp = dp_engine.DiscreteLaplaceDifferentialPrivacy(epsilon=0.7)

ZONE_AREAS = {
    "A": 50,
    "B": 40,
    "C": 30
}

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.json
    results = []

    for zone_id, true_count in data["zones"].items():

        # Apply DP
        dp_count = dp.privatize_count(true_count)

        # recompute density using DP count (important)
        dp_density = dp_count / ZONE_AREAS[zone_id]

        event = {
            "location_id": data["location_id"],
            "scenario_id": data["scenario_id"],
            "timestamp": data["time"],
            "zone_id": zone_id,
            "dp_count": dp_count,
            "density": round(dp_density, 2),
            "speed": data["speed"][zone_id],
            "decision": dp_engine.classify(dp_count, dp_density),
            "event_type": data["event"],
            "epsilon": dp.epsilon
        }

        # Send ONLY DP data to external API
        try:
            res = requests.post(EXTERNAL_API_URL, json=event)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Failed to send to external API:", e)

        results.append(event)

    return jsonify({
        "status": "processed",
        "zones_processed": len(results)
    })


if __name__ == "__main__":
    app.run(debug=True)