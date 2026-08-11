"""A rational two-transaction counterexample and its machine certificate."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from .confidence import (
    ReleasedApproxKellyLogicalN2,
    first_round_combined_interval,
    released_approx_kelly_initial_bet,
)
from .dp import TerminalPath, enumerate_terminal_paths, expected_audit_length
from .model import AuditInstance
from .n2 import characterize_n2
from .policies import (
    FixedFirstDistributionPolicy,
    OracleContributionPolicy,
    ProportionalValuePolicy,
)

COUNTEREXAMPLE = AuditInstance.from_values(
    weights=("3/4", "1/4"),
    misstatements=("1/3", "1"),
    epsilon="1/3",
    delta="1/20",
)


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def decimal_text(value: Fraction, places: int = 12) -> str:
    return f"{float(value):.{places}f}".rstrip("0").rstrip(".")


def _path_record(path: TerminalPath) -> dict[str, Any]:
    return {
        "history_1_based": [index + 1 for index in path.history],
        "probability": fraction_text(path.probability),
        "stopping_time": path.stopping_time,
        "final_logical_interval": [
            fraction_text(path.final_interval.lower),
            fraction_text(path.final_interval.upper),
        ],
        "final_diameter": fraction_text(path.final_interval.diameter),
    }


def build_certificate() -> dict[str, Any]:
    instance = COUNTEREXAMPLE
    stopping_rule = ReleasedApproxKellyLogicalN2()
    oracle = OracleContributionPolicy()
    alternative = ProportionalValuePolicy()
    deterministic = FixedFirstDistributionPolicy.from_values(
        (1, 0), "deterministic-large-first"
    )
    eta = Fraction(1, 100)
    eta_policy = FixedFirstDistributionPolicy.from_values(
        (1 - eta, eta), "eta-full-support"
    )

    oracle_distribution = oracle.probabilities(instance, ())
    alternative_distribution = alternative.probabilities(instance, ())
    oracle_paths = enumerate_terminal_paths(instance, oracle, stopping_rule)
    alternative_paths = enumerate_terminal_paths(instance, alternative, stopping_rule)
    oracle_expectation = expected_audit_length(instance, oracle, stopping_rule)
    alternative_expectation = expected_audit_length(instance, alternative, stopping_rule)
    deterministic_paths = enumerate_terminal_paths(
        instance, deterministic, stopping_rule, support_mode="simplex"
    )
    deterministic_expectation = expected_audit_length(
        instance, deterministic, stopping_rule, support_mode="simplex"
    )
    eta_paths = enumerate_terminal_paths(
        instance, eta_policy, stopping_rule, support_mode="full"
    )
    eta_expectation = expected_audit_length(
        instance, eta_policy, stopping_rule, support_mode="full"
    )
    characterization = characterize_n2(instance)
    gap = oracle_expectation - alternative_expectation
    ratio = alternative_expectation / oracle_expectation

    if not gap > 0:
        raise AssertionError("counterexample inequality is not strict")

    first_intervals = {
        str(index + 1): first_round_combined_interval(instance, index)
        for index in range(instance.size)
    }

    return {
        "schema_version": 2,
        "result": "counterexample",
        "claim": (
            "The repeated q_t(i) proportional to pi_i f_i oracle is not globally "
            "optimal for expected audit length under the authors' released "
            "ApproxKelly initialization intersected with the logical CS."
        ),
        "construction": {
            "betting_rule": "ApproxKelly",
            "initial_bet": fraction_text(released_approx_kelly_initial_bet()),
            "confidence_sequence": (
                "betting CS intersected with logical CS and running intersection"
            ),
            "stopping_rule": "first t with diameter(C_t) <= epsilon",
        },
        "policy_class_audit": {
            "literal_definition": (
                "Definition 2 permits a probability distribution on the remaining set; "
                "the Proposition 2 action space is the simplex of such distributions."
            ),
            "simplex_boundary": "deterministic first-stage distributions are included",
            "conservative_variants": [
                "positive probability on every positive-contribution item",
                "strictly positive probability on every remaining item",
            ],
        },
        "instance": {
            "N": instance.size,
            "pi": [fraction_text(value) for value in instance.weights],
            "f": [fraction_text(value) for value in instance.misstatements],
            "epsilon": fraction_text(instance.epsilon),
            "delta": fraction_text(instance.delta),
            "m_star": fraction_text(instance.total_misstatement),
            "pi_times_f": [
                fraction_text(instance.contribution(index)) for index in range(instance.size)
            ],
        },
        "first_round": {
            "betting_CS": ["0", "1"],
            "combined_CS_by_sampled_item": {
                label: {
                    "interval": [fraction_text(interval.lower), fraction_text(interval.upper)],
                    "diameter": fraction_text(interval.diameter),
                    "stops": interval.diameter <= instance.epsilon,
                }
                for label, interval in first_intervals.items()
            },
        },
        "policies": {
            "oracle-pi-f": {
                "first_distribution": [
                    fraction_text(oracle_distribution[index]) for index in range(instance.size)
                ],
                "terminal_paths": [_path_record(path) for path in oracle_paths],
                "expected_tau": fraction_text(oracle_expectation),
                "expected_tau_decimal": decimal_text(oracle_expectation),
            },
            "prop-M": {
                "first_distribution": [
                    fraction_text(alternative_distribution[index])
                    for index in range(instance.size)
                ],
                "terminal_paths": [_path_record(path) for path in alternative_paths],
                "expected_tau": fraction_text(alternative_expectation),
                "expected_tau_decimal": decimal_text(alternative_expectation),
            },
            "deterministic-large-first": {
                "support_convention": "literal simplex",
                "first_distribution": ["1", "0"],
                "terminal_paths": [_path_record(path) for path in deterministic_paths],
                "expected_tau": fraction_text(deterministic_expectation),
            },
            "eta-full-support": {
                "eta": fraction_text(eta),
                "support_convention": "strict full support",
                "first_distribution": [fraction_text(1 - eta), fraction_text(eta)],
                "terminal_paths": [_path_record(path) for path in eta_paths],
                "expected_tau": fraction_text(eta_expectation),
            },
        },
        "comparison": {
            "strict_inequality": "5/4 < 3/2",
            "oracle_minus_prop_M": fraction_text(gap),
            "prop_M_over_oracle": fraction_text(ratio),
            "relative_reduction": fraction_text(gap / oracle_expectation),
        },
        "global_N2_solution": {
            "first_stage_formula": (
                "E[tau(q)] = 2 - sum_{i: 1-pi_i <= epsilon} q(i)"
            ),
            "stopping_items_1_based": [
                index + 1 for index in characterization.stopping_items
            ],
            "literal_simplex": {
                "minimum": fraction_text(characterization.optimal_value),
                "attained": characterization.unrestricted_attained,
                "one_optimal_distribution": ["1", "0"],
                "oracle_minus_minimum": fraction_text(
                    oracle_expectation - characterization.optimal_value
                ),
            },
            "positive_contribution_support": {
                "infimum": fraction_text(characterization.importance_support_infimum),
                "attained": characterization.importance_support_attained,
            },
            "strict_full_support": {
                "infimum": fraction_text(characterization.full_support_infimum),
                "attained": characterization.full_support_attained,
                "approaching_family": "q_eta = (1-eta, eta), E[tau] = 1+eta",
            },
            "delta_dependence": "none for N=2 under the pinned zero first bet",
            "f_dependence": "none for the optimal policy; f only changes comparator policies",
        },
    }


def certificate_json() -> str:
    return json.dumps(build_certificate(), indent=2, sort_keys=True) + "\n"


def write_certificate(path: str | Path) -> None:
    Path(path).write_text(certificate_json(), encoding="utf-8")
