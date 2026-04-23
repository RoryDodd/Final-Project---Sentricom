import random
import math


class LaplaceDifferentialPrivacy:
    #Standard Laplace mechanism - adds continuous noise drawn from a Laplace distribution.
    def __init__(self, epsilon):
        self.epsilon = epsilon          # Privacy budget - lower = more private, more noise
        self.sensitivity = 1            # How much one person affects the count

    def privatize_count(self, true_count):
        #Add Laplace noise to the true count and return a private integer count.
        scale = self.sensitivity / self.epsilon     # Higher scale = more noise
        noise = self.laplace_noise(scale)
        return max(0, int(true_count + noise))      # Limit to 0, can't have negative people

    def laplace_noise(self, scale):
        #Generate a random noise value from a Laplace distribution.
        u = random.random() - 0.5      # Random value between -0.5 and 0.5
        return -scale * math.copysign(1, u) * math.log(1 - 2 * abs(u))


class GaussianDifferentialPrivacy:
    """Gaussian mechanism - adds noise from a normal distribution.
    Requires a delta parameter, allowing a small probability of privacy breach."""
    def __init__(self, epsilon, delta):
        self.epsilon = epsilon          # Privacy budget
        self.delta = delta              # Small allowed probability of privacy breach (e.g. 1e-5)
        self.sensitivity = 1
        '''Sigma is the standard deviation of the Gaussian noise
        Larger sigma = more noise = more privacy'''
        self.sigma = self.sensitivity * math.sqrt(2 * math.log(1.25 / delta)) / epsilon

    def privatize_count(self, true_count):
        #Add Gaussian noise to the true count and return a private integer count.
        noise = random.gauss(0, self.sigma)     # Noise centred at 0 with std deviation sigma
        return max(0, int(true_count + noise))


class DiscreteLaplaceDifferentialPrivacy:
    """Discrete Laplace mechanism - like Laplace but noise is always a whole integer.
    More accurate for counting people since you can't have fractions of a person."""
    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.sensitivity = 1
        self.scale = math.exp(-epsilon / self.sensitivity)  # Controls the spread of noise

    def privatize_count(self, true_count):
        #Add discrete integer noise to the true count and return a private integer count.
        noise = self.discrete_laplace_noise()
        return max(0, int(true_count + noise))

    def discrete_laplace_noise(self):
        '''Generate integer noise using the geometric mechanism.
        Difference of two geometric random variables gives discrete Laplace noise.
        Two geometric samples, their difference gives symmetric integer noise'''
        geo1 = math.floor(math.log(random.random()) / math.log(self.scale))
        geo2 = math.floor(math.log(random.random()) / math.log(self.scale))
        return geo1 - geo2  # Subtract to centre noise around 0


def classify(count, density):
    #Classify the crowd situation based on DP count and area density.
    if density > 2.5:
        return "EVACUATE"
    elif count >= 20:
        return "MONITOR"
    return "SAFE"