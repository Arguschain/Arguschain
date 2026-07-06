"""benford_engine.py."""
"""Benford's Law feature computation engine."""
import logging
from collections import Counter
import numpy as np
from scipy import stats
from detection.benford_baseline import BENFORD_EXPECTED_FREQUENCIES, CHI_SQUARE_DF

logger = logging.getLogger("arguschain.detection.benford_engine")

class BenfordEngine:
    def __init__(self, min_transactions: int = 20):
        self.min_transactions = min_transactions

    def extract_leading_digit(self, amount: float):
        if amount <= 0:
            return None
        amount_str = str(abs(int(amount)))
        for char in amount_str:
            if char.isdigit() and char != "0":
                return int(char)
        return None

    def compute_chi_square(self, amounts):
        if len(amounts) < self.min_transactions:
            return 0.0, 1.0, "insufficient_data"
        leading_digits = [d for a in amounts if (d := self.extract_leading_digit(a))]
        if len(leading_digits) < self.min_transactions:
            return 0.0, 1.0, "insufficient_digits"
        digit_counts = Counter(leading_digits)
        observed = np.array([digit_counts.get(d, 0) for d in range(1, 10)])
        expected = np.array([BENFORD_EXPECTED_FREQUENCIES[d] * len(leading_digits) for d in range(1, 10)])
        chi_square = np.sum((observed - expected) ** 2 / expected)
        if len(leading_digits) < 100:
            p_value = self._bootstrap_pvalue(observed, expected, 10000)
            method = "bootstrap"
        else:
            p_value = 1.0 - stats.chi2.cdf(chi_square, CHI_SQUARE_DF)
            method = "asymptotic"
        return chi_square, p_value, method

    def _bootstrap_pvalue(self, observed, expected, n_samples=10000):
        total = np.sum(observed)
        expected_probs = expected / np.sum(expected)
        test_stat_obs = np.sum((observed - expected) ** 2 / expected)
        count_extreme = sum(1 for _ in range(n_samples)
                           if np.sum((np.random.multinomial(total, expected_probs) - expected) ** 2 / expected) >= test_stat_obs)
        return count_extreme / n_samples

    def compute_mad(self, amounts):
        if len(amounts) < self.min_transactions:
            return 0.0
        leading_digits = [d for a in amounts if (d := self.extract_leading_digit(a))]
        if len(leading_digits) < self.min_transactions:
            return 0.0
        digit_counts = Counter(leading_digits)
        mad = sum(abs(digit_counts.get(d, 0) / len(leading_digits) - BENFORD_EXPECTED_FREQUENCIES[d]) for d in range(1, 10))
        return mad / 9.0
