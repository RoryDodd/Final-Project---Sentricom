import random
import math


class LaplaceDifferentialPrivacy:
    def __init__(self, epsilon: float, sensitivity: float = 1.0):
        self.epsilon = epsilon
        self.sensitivity = sensitivity
        self.scale = sensitivity / epsilon

    def laplace_noise(self) -> float:
        u = random.random() - 0.5
        return -self.scale * math.copysign(1, u) * math.log(1 - 2 * abs(u))

    def privatize_count(self, true_count: int) -> int:
        return max(0, round(true_count + self.laplace_noise()))

    @staticmethod
    def classify(count: int) -> str:
        if count > 50:
            return "EVACUATE"
        if count >= 25:
            return "MONITOR"
        return "LOW RISK"


class GaussianDifferentialPrivacy:
    def __init__(self, epsilon: float, delta: float = 1e-5, sensitivity: float = 1.0):
        self.epsilon = epsilon
        self.delta = delta
        self.sensitivity = sensitivity
        # For (epsilon, delta)-DP, sigma = sensitivity * sqrt(2 * ln(1.25 / delta)) / epsilon
        self.sigma = sensitivity * math.sqrt(2 * math.log(1.25 / delta)) / epsilon

    def gaussian_noise(self) -> float:
        # Box-Muller transform for Gaussian noise
        u1 = random.random()
        u2 = random.random()
        z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        return z0 * self.sigma

    def privatize_count(self, true_count: int) -> int:
        return max(0, round(true_count + self.gaussian_noise()))

    @staticmethod
    def classify(count: int) -> str:
        if count > 50:
            return "EVACUATE"
        if count >= 25:
            return "MONITOR"
        return "LOW RISK"
