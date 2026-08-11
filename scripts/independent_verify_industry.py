#!/usr/bin/env python3
"""Independent exact verifier; deliberately does not import the package."""

from __future__ import annotations

import json
from fractions import Fraction
from functools import cache
from itertools import combinations, permutations
from pathlib import Path


def f(text: str | int) -> Fraction:
    return Fraction(text)


def text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


record = json.loads(Path("certificates/industry-results.json").read_text())

# Sharp oracle family.
sharp = record["sharp_oracle_lower_bound"]
instance = sharp["instance"]
n = instance["N"]
rho = f(sharp["sharpness"]["rho"])
epsilon = Fraction(1, 20 * n)
a = epsilon / 2
p = 1 - a
w = a / (n - 1)
assert f(instance["epsilon"]) == epsilon
assert f(instance["delta"]) == Fraction(1, 20)
assert tuple(map(f, instance["pi"])) == (p,) + (w,) * (n - 1)
assert tuple(map(f, instance["f"])) == (rho * w / p,) + (Fraction(1),) * (n - 1)

oracle_expected = 1 + Fraction(n - 1, 1) / (1 + rho)
prop_m_rank = 1 + Fraction(n - 1, 1) * w / (p + w)
assert sharp["expected_lengths"]["oracle"] == text(oracle_expected)
assert sharp["expected_lengths"]["prop_M_upper_bound_via_large_item_rank"] == text(
    prop_m_rank
)
witnesses = tuple(map(f, sharp["surviving_grid_witnesses"]["candidates"]))
assert witnesses == (a, 5 * a)
assert witnesses[1] - witnesses[0] == 2 * epsilon
wealth_bound = (1 + Fraction(1, 4 * n)) ** n
assert sharp["surviving_grid_witnesses"]["uniform_wealth_upper_bound"] == text(
    wealth_bound
)
assert wealth_bound < 2 < 20

# Certified interval example.
robust = record["certified_score_minimax"]
box = robust["instance"]
weights = tuple(map(f, box["pi"]))
lower = tuple(map(f, box["lower"]))
upper = tuple(map(f, box["upper"]))
epsilon = f(box["epsilon"])
d = tuple(
    weight * (hi - lo)
    for weight, lo, hi in zip(weights, lower, upper, strict=True)
)
total = sum(d, Fraction(0))
assert tuple(map(f, box["uncertainty_contributions"])) == d


def stopping_time(order: tuple[int, ...]) -> int:
    residual = total
    if residual <= epsilon:
        return 0
    for time, index in enumerate(order, start=1):
        residual -= d[index]
        if residual <= epsilon:
            return time
    raise AssertionError


minimum = min(stopping_time(order) for order in permutations(range(len(d))))
assert robust["unit_cost_solution"]["minimum_reviews"] == minimum


@cache
def expected(remaining: frozenset[int]) -> Fraction:
    residual = sum((d[index] for index in remaining), Fraction(0))
    if residual <= epsilon:
        return Fraction(0)
    denominator = residual
    return 1 + sum(
        (d[index] / denominator) * expected(remaining - {index}) for index in remaining
    )


randomized = expected(frozenset(range(len(d))))
randomized_record = robust["unit_cost_solution"][
    "expected_reviews_if_randomized_proportional_to_uncertainty"
]
assert randomized_record == text(randomized)

costs = tuple(map(f, robust["heterogeneous_cost_solution"]["costs"]))
target = total - epsilon
feasible: list[tuple[Fraction, tuple[int, ...]]] = []
for size in range(len(d) + 1):
    for selected in combinations(range(len(d)), size):
        if sum((d[index] for index in selected), Fraction(0)) >= target:
            feasible.append(
                (sum((costs[index] for index in selected), Fraction(0)), selected)
            )
minimum_cost = min(value[0] for value in feasible)
assert robust["heterogeneous_cost_solution"]["total_cost"] == text(minimum_cost)

print("independently verified sharp oracle and certified-score theorems")
