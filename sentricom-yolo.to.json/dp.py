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
    def __init__(self, epsilon: float, delta: float, sensitivity: float = 1.0):
        self.epsilon = epsilon
        self.sensitivity = sensitivity
        self.delta = delta
        self.sigma = sensitivity * math.sqrt(2 * math.log(1.25 / delta)) / epsilon

    def privatize_count(self, true_count: int) -> int:
        noise = random.gauss(0, self.sigma)
        return max(0, round(true_count + noise))
    
    @staticmethod
    def classify(count: int) -> str:
        if count > 50:
            return "EVACUATE"
        if count >= 25:
            return "MONITOR"
        return "LOW RISK"