import numpy as np
from scipy.stats import norm

class BlackScholes(object):

    def __init__(self, S, K, t, sigma, r, delta):
        print(t)

        self.S = S
        self.K = K
        self.t = t
        self.sigma = sigma
        self.r = r
        self.delta = delta

    def d1(self):
        numerator = np.log(self.S / self.K) + (self.r - self.delta + 0.5 * (self.sigma ** 2)) * self.t
        denominator = self.sigma * np.sqrt(self.t)
        return numerator / denominator

    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.t)

    def call_price(self):
        return (self.S * np.exp(-self.delta * self.t) * norm.cdf(self.d1()) -
                self.K * np.exp(-self.r * self.t) * norm.cdf(self.d2()))

    def put_price(self):
        return (self.K * np.exp(-self.r * self.t) * norm.cdf(-self.d2()) -
                self.S * np.exp(-self.delta * self.t) * norm.cdf(-self.d1()))
