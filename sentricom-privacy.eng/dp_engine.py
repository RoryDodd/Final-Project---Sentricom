import random
import math

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
        u = random.random() - 0.5
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
        geo1 = math.floor(math.log(random.random()) / math.log(self.scale))
        geo2 = math.floor(math.log(random.random()) / math.log(self.scale))
        return geo1 - geo2


def classify(count, density):
    #Classify the crowd situation based on DP count and area density.
    if density > 2.5:
        return "EVACUATE"
    elif count >= 20:
        return "MONITOR"
    return "SAFE"