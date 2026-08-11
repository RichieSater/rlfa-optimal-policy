#!/usr/bin/env python3
"""Reproducible synthetic workload benchmark for certified-score policies."""

from __future__ import annotations

import json
import math
import random
import statistics
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Scenario:
    name: str
    size: int
    relative_error: float
    residual_fraction: float
    value_sigma: float
    score_mode: str
    seed: int


SCENARIOS = (
    Scenario("unclipped-concentrated", 1000, 0.25, 0.10, 1.5, "low", 20260811),
    Scenario("clipped-high-risk", 1000, 0.40, 0.10, 1.5, "high", 20260812),
    Scenario("diffuse-values", 1000, 0.25, 0.10, 0.15, "low", 20260813),
    Scenario("tight-certificate", 1000, 0.25, 0.02, 1.5, "low", 20260814),
)
REPETITIONS = 1000


def population(scenario: Scenario) -> tuple[list[float], list[float], list[float], list[float]]:
    rng = random.Random(scenario.seed)
    raw_weights = [math.exp(rng.gauss(0, scenario.value_sigma)) for _ in range(scenario.size)]
    total_weight = sum(raw_weights)
    weights = [value / total_weight for value in raw_weights]
    if scenario.score_mode == "low":
        scores = [0.01 + 0.54 * rng.betavariate(2, 5) for _ in range(scenario.size)]
    elif scenario.score_mode == "high":
        scores = [0.25 + 0.74 * rng.betavariate(5, 2) for _ in range(scenario.size)]
    else:  # pragma: no cover - fixed scenario table
        raise ValueError("unknown score mode")
    a = scenario.relative_error
    lower = [score / (1 + a) for score in scores]
    upper = [min(1.0, score / (1 - a)) for score in scores]
    actual = [(lo + hi) / 2 for lo, hi in zip(lower, upper, strict=True)]
    uncertainty = [
        weight * (hi - lo)
        for weight, lo, hi in zip(weights, lower, upper, strict=True)
    ]
    return weights, scores, actual, uncertainty


def stopping_time(order: list[int], uncertainty: list[float], target: float) -> int:
    removed = 0.0
    for time, index in enumerate(order, start=1):
        removed += uncertainty[index]
        if removed + 1e-15 >= target:
            return time
    return len(order)


def pps_order(rates: list[float], rng: random.Random) -> list[int]:
    # Independent exponential clocks generate the exact Plackett--Luce order.
    keys = [(-math.log1p(-rng.random()) / rate, index) for index, rate in enumerate(rates)]
    keys.sort()
    return [index for _, index in keys]


def summarize(values: list[int], optimum: int) -> dict[str, float | int]:
    ordered = sorted(values)
    mean = statistics.fmean(values)
    standard_deviation = statistics.stdev(values)
    return {
        "mean_reviews": mean,
        "standard_deviation": standard_deviation,
        "standard_error": standard_deviation / math.sqrt(len(values)),
        "median_reviews": statistics.median(values),
        "p95_reviews": ordered[math.ceil(0.95 * len(ordered)) - 1],
        "mean_over_optimum": mean / optimum,
        "extra_reviews_over_optimum": mean - optimum,
    }


def main() -> None:
    output_cases = []
    for scenario in SCENARIOS:
        weights, scores, actual, uncertainty = population(scenario)
        total_uncertainty = sum(uncertainty)
        epsilon = scenario.residual_fraction * total_uncertainty
        target = total_uncertainty - epsilon
        optimal_order = sorted(range(scenario.size), key=lambda index: -uncertainty[index])
        optimum = stopping_time(optimal_order, uncertainty, target)
        policies = {
            "uncertainty-PPS": uncertainty,
            "prop-MS": [
                weight * score for weight, score in zip(weights, scores, strict=True)
            ],
            "prop-M": weights,
            "oracle-pi-f": [
                weight * value for weight, value in zip(weights, actual, strict=True)
            ],
            "uniform": [1.0] * scenario.size,
        }
        policy_results = {}
        for offset, (name, rates) in enumerate(policies.items(), start=1):
            rng = random.Random(scenario.seed + 100000 * offset)
            values = [
                stopping_time(pps_order(rates, rng), uncertainty, target)
                for _ in range(REPETITIONS)
            ]
            policy_results[name] = summarize(values, optimum)
        output_cases.append(
            {
                "name": scenario.name,
                "N": scenario.size,
                "relative_error": scenario.relative_error,
                "residual_fraction_of_initial_width": scenario.residual_fraction,
                "value_log_sigma": scenario.value_sigma,
                "score_mode": scenario.score_mode,
                "seed": scenario.seed,
                "initial_box_width": total_uncertainty,
                "epsilon": epsilon,
                "optimal_descending_uncertainty_reviews": optimum,
                "randomized_policies": policy_results,
            }
        )
    output = {
        "schema_version": 1,
        "repetitions_per_policy": REPETITIONS,
        "stopping_rule": "remaining simultaneous-box width <= epsilon",
        "caveat": (
            "Synthetic benchmark, not an empirical claim about a particular audit population. "
            "Monte Carlo affects only randomized comparator policies; the optimum is exact."
        ),
        "cases": output_cases,
    }
    path = Path("benchmarks/certified-score-synthetic.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(path)


if __name__ == "__main__":
    main()
