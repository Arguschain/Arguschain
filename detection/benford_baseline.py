"""benford_baseline.py."""
# Expected frequency of leading digits 1-9 under Benford's Law
BENFORD_EXPECTED_FREQUENCIES = {
    1: 0.30103, 2: 0.17609, 3: 0.12494, 4: 0.09691, 5: 0.07918,
    6: 0.06695, 7: 0.05799, 8: 0.05115, 9: 0.04576,
}
CHI_SQUARE_DF = 8
CHI_SQUARE_CRITICAL_05 = 15.507
