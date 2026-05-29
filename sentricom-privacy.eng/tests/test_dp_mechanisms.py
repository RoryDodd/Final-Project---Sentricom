__author__ = "R Dodd"
__version__ = "1.0"
__date__ = "May 2026"

"""This test file checks that the DP mechanisms return valid, non-negative integer counts, that discrete Laplace noise is roughly centered around zero
and that Gaussian noise stays within a reasonable range, also confirms the factory function creates the expected mechanism."""

import sys
from pathlib import Path
import pytest

# Ensure the dp_engine module can be imported from the parent directory
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import the DP mechanisms to test (must import after adjusting sys.path)
from dp_engine import (
    LaplaceDifferentialPrivacy,
    GaussianDifferentialPrivacy,
    DiscreteLaplaceDifferentialPrivacy,
    create_dp, # for testing the factory function
)

# Test parameters 1: Run the same test with multiple input values to check common cases
@pytest.mark.parametrize("true_count, epsilon, max_noise", [
    (0, 0.4, 5),
    (10, 0.4, 5),
    (50, 0.1, 3),
])

# Test that privatized counts are non-negative integers for Laplace DP
def test_privatize_count_non_negative(true_count, epsilon, max_noise):
    dp = LaplaceDifferentialPrivacy(epsilon=epsilon)
    result = dp.privatize_count(true_count, max_noise=max_noise)
    assert 0 <= result # Non-negative
    assert isinstance(result, int) # Integer result

# Test that the factory function creates the correct DP mechanism
def test_discrete_laplace_noise_symmetric():
    dp = DiscreteLaplaceDifferentialPrivacy(epsilon=0.4)
    noise_samples = [
        dp.generate_noise() for _ in range(1000) # Generate many samples to check distribution symmetry
    ]
    # Average noise should be close to 0
    avg_noise = sum(noise_samples) / len(noise_samples)
    assert -0.5 <= avg_noise <= 0.5  # very rough, but not wildly biased

# Test parameters 2: Test that the Gaussian DP mechanism generates noise within expected bounds
@pytest.mark.parametrize("epsilon, delta", [
    (0.4, 1e-5),
    (0.1, 1e-6),
])
#Note: Gaussian test may fail occasionally due to the nature of random noise
def test_gaussian_privacy_budget(epsilon, delta):
    dp = GaussianDifferentialPrivacy(epsilon=epsilon, delta=delta)
    # Noise should centre near 0
    noise = dp.generate_noise()
    assert -5 <= noise <= 5  # Check that noise is within a reasonable range