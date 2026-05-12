__author__ = "R Dodd", "Richard Avery"
__version__ = "2.0"
__date__ = "2026"

import random
import math
import api

class DifferentialPrivacy:
    #Base class containing shared logic for all DP mechanisms.
    
    def privatize_count(self, true_count, max_noise=10):
        # Clamp the noise to a range of -max_noise to max_noise to prevent extreme outliers
        noise = max(-max_noise, min(max_noise, self.generate_noise()))
        # Add noise to the true count, ensuring the result is never negative
        return max(0, int(true_count + noise))
    
    def generate_noise(self):
        # Forces each subclass to implement their own noise generation method
        raise NotImplementedError("Subclass must implement generate_noise()")


class LaplaceDifferentialPrivacy(DifferentialPrivacy):
    #Standard Laplace mechanism - adds continuous noise drawn from a Laplace distribution.
    def __init__(self, epsilon):
        self.epsilon = epsilon      # Privacy budget - lower = more private, more noise
        self.sensitivity = 1        # How much one person affects the count

    def generate_noise(self):
        scale = self.sensitivity / self.epsilon
        u = random.random() - 0.5   # nosec B311
        return -scale * math.copysign(1, u) * math.log(1 - 2 * abs(u))


class GaussianDifferentialPrivacy(DifferentialPrivacy):
    """Gaussian mechanism - adds noise from a normal distribution.
    Requires a delta parameter, allowing a small probability of privacy breach."""
    def __init__(self, epsilon, delta):
        self.epsilon = epsilon          # Privacy budget
        self.delta = delta              # Small allowed probability of privacy breach (e.g. 1e-5)
        self.sensitivity = 1
        self.sigma = self.sensitivity * math.sqrt(2 * math.log(1.25 / delta)) / epsilon

    def generate_noise(self):
        # Noise centred at 0 with std deviation sigma
        return random.gauss(0, self.sigma)


class DiscreteLaplaceDifferentialPrivacy(DifferentialPrivacy):
    """Discrete Laplace mechanism - like Laplace but noise is always a whole integer.
    More accurate for counting people since you can't have fractions of a person."""
    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.sensitivity = 1
        self.scale = math.exp(-epsilon / self.sensitivity)

    def generate_noise(self):
        '''Generate integer noise using the geometric mechanism.
        Difference of two geometric random variables gives discrete Laplace noise.
        Two geometric samples, their difference gives symmetric integer noise'''
        geo1 = math.floor(math.log(random.random()) / math.log(self.scale)) # nosec B311
        geo2 = math.floor(math.log(random.random()) / math.log(self.scale)) # nosec B311
        return geo1 - geo2


def classify(count, density):
    #Classify the crowd situation based on DP count and area density.
    if density > 2.5:
        return "EVACUATE"
    elif count >= 20:
        return "MONITOR"
    return "SAFE"


def create_dp(config):
    """Factory function to create a DP mechanism based on config."""
    if config["mechanism"] == "laplace":
        return LaplaceDifferentialPrivacy(epsilon=config["epsilon"])
    elif config["mechanism"] == "gaussian":
        return GaussianDifferentialPrivacy(epsilon=config["epsilon"], delta=config["delta"])
    elif config["mechanism"] == "discrete_laplace":
        return DiscreteLaplaceDifferentialPrivacy(epsilon=config["epsilon"])
    else:
        raise ValueError("Unknown DP mechanism specified")
    
# ---------------------------------------------------------------------------
# DP Processing
# ---------------------------------------------------------------------------

def process_through_dp(zone_data, dp_config=None):
    """Apply differential privacy to a batch of zone data."""
    if not dp_config:
        dp_config = api.DEFAULT_DP_CONFIG

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
        zone_area = api.ZONE_AREAS.get(zone_key, 50)

        # Apply DP noise
        dp_count = dp.privatize_count(real_count)

        # Recalculate density using DP count
        dp_density = dp_count / zone_area

        # Classify risk
        risk_level = classify(dp_count, dp_density)

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