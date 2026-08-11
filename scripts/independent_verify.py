#!/usr/bin/env python3
"""Independently verify the checked certificate without importing the package."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


def q(value: str) -> Fraction:
    return Fraction(value)


root = Path(__file__).resolve().parents[1]
certificate = json.loads((root / "certificates/counterexample.json").read_text())

instance = certificate["instance"]
pi = tuple(q(value) for value in instance["pi"])
f = tuple(q(value) for value in instance["f"])
epsilon = q(instance["epsilon"])
delta = q(instance["delta"])

assert instance["N"] == 2
assert all(weight > 0 for weight in pi)
assert sum(pi) == 1
assert all(0 <= value <= 1 for value in f)
assert 0 < epsilon < 1
assert 0 < delta < 1

contributions = tuple(pi[index] * f[index] for index in range(2))
assert contributions == tuple(q(value) for value in instance["pi_times_f"])
assert sum(contributions) == q(instance["m_star"])
assert q(certificate["construction"]["initial_bet"]) == 0

# With lambda_1 = 0, the betting CS is [0,1]. The logical first-round
# diameters are the weights of the other transaction.
diameter_if_first = (pi[1], pi[0])
stops_if_first = tuple(diameter <= epsilon for diameter in diameter_if_first)
assert stops_if_first == (True, False)

oracle_distribution = tuple(
    contribution / sum(contributions) for contribution in contributions
)
prop_m_distribution = pi
assert oracle_distribution == tuple(
    q(value) for value in certificate["policies"]["oracle-pi-f"]["first_distribution"]
)
assert prop_m_distribution == tuple(
    q(value) for value in certificate["policies"]["prop-M"]["first_distribution"]
)


def expected_tau(distribution: tuple[Fraction, Fraction]) -> Fraction:
    # Item 1 (index 0) stops at t=1. Item 2 requires the complete audit at t=2.
    return distribution[0] + 2 * distribution[1]


oracle_expected = expected_tau(oracle_distribution)
prop_m_expected = expected_tau(prop_m_distribution)
deterministic_distribution = tuple(
    q(value)
    for value in certificate["policies"]["deterministic-large-first"][
        "first_distribution"
    ]
)
eta_distribution = tuple(
    q(value)
    for value in certificate["policies"]["eta-full-support"]["first_distribution"]
)
deterministic_expected = expected_tau(deterministic_distribution)
eta_expected = expected_tau(eta_distribution)
assert oracle_expected == q(certificate["policies"]["oracle-pi-f"]["expected_tau"])
assert prop_m_expected == q(certificate["policies"]["prop-M"]["expected_tau"])
assert deterministic_expected == q(
    certificate["policies"]["deterministic-large-first"]["expected_tau"]
)
assert eta_expected == q(certificate["policies"]["eta-full-support"]["expected_tau"])
assert oracle_expected == Fraction(3, 2)
assert prop_m_expected == Fraction(5, 4)
assert deterministic_expected == 1
assert eta_expected == Fraction(101, 100)
assert prop_m_expected < oracle_expected
assert oracle_expected - prop_m_expected == Fraction(1, 4)
assert q(certificate["global_N2_solution"]["literal_simplex"]["minimum"]) == 1
assert certificate["global_N2_solution"]["literal_simplex"]["attained"]
assert q(certificate["global_N2_solution"]["strict_full_support"]["infimum"]) == 1
assert not certificate["global_N2_solution"]["strict_full_support"]["attained"]

print("independent exact verification passed: 1 < 5/4 < 3/2")
