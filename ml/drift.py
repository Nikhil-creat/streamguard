"""Population Stability Index between baseline and live score distributions. PSI > 0.2 signals drift."""
import numpy as np
def psi(base, live, bins=10):
    edges = np.linspace(0, 1, bins + 1)
    b, l = (np.histogram(x, edges)[0] / len(x) + 1e-6 for x in (base, live))
    return float(np.sum((l - b) * np.log(l / b)))
if __name__ == "__main__":
    print("psi", round(psi(np.random.beta(2, 8, 5000), np.random.beta(2, 7, 5000)), 4))
