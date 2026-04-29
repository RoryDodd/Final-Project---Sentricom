from flask import Flask, request, jsonify
import requests
import dp_engine

app = Flask(__name__)

# Your teammate's API endpoint (replace this)
EXTERNAL_API_URL = "http://external-service/api/events"

def create_dp(config):
    if config["mechanism"] == "laplace":
        return dp_engine.LaplaceDifferentialPrivacy(epsilon=config["epsilon"])
    elif config["mechanism"] == "gaussian":
        return dp_engine.GaussianDifferentialPrivacy(epsilon=config["epsilon"], delta=config["delta"])
    elif config["mechanism"] == "discrete_laplace":
        return dp_engine.DiscreteLaplaceDifferentialPrivacy(epsilon=config["epsilon"])
    else:
        raise ValueError("Unknown DP mechanism specified")


ZONE_AREAS = {
    "A": 50,
    "B": 40,
    "C": 30
}

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.json
    results = []

    config = data.get("dp_config", {})
    dp = create_dp(config)


    for zone_id, true_count in data["raw_counts"].items():

        # Apply DP
        dp_count = dp.privatize_count(true_count)
        # recompute density using DP count (important)
        dp_density = dp_count / ZONE_AREAS[zone_id]

        risk_level = dp_engine.classify(dp_count, dp_density)

        event = {
            "location_id": data["location_id"],
            "scenario_id": data["scenario_id"],
            "time": data["time"],
            "zone_id": zone_id,

            "dp_count": dp_count,
            "density": round(dp_density, 2),
            "speed": data["speed"][zone_id],

            "risk_level": risk_level,
            "event_type": data["event"],

            "epsilon": dp.epsilon,
            "mechanism": config.get("mechanism", "discrete_laplace")
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