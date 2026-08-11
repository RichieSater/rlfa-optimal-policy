#!/usr/bin/env python3
"""Generate exact small-N policy comparisons for the augmented-state solver."""

from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from rlfa_optimal_policy.approxkelly import (
    ApproxKellyConfig,
    evaluate_policy,
    solve_action_mesh,
)
from rlfa_optimal_policy.counterexample import decimal_text, fraction_text
from rlfa_optimal_policy.model import AuditInstance
from rlfa_optimal_policy.policies import (
    MeshPriorityPolicy,
    OracleContributionPolicy,
    ProportionalMonetaryScorePolicy,
    ProportionalValuePolicy,
)
from rlfa_optimal_policy.robust import multiplicative_score_box


@dataclass(frozen=True)
class Case:
    name: str
    instance: AuditInstance
    scores: tuple[Fraction, ...]
    relative_error: Fraction


CASES = (
    Case(
        "terminal-value-n3",
        AuditInstance.from_values(
            ("1/2", "1/3", "1/6"),
            ("1/6", "1/4", "1"),
            "1/3",
            "1/20",
        ),
        (Fraction(1, 5), Fraction(1, 5), Fraction(9, 10)),
        Fraction(1, 4),
    ),
    Case(
        "mixed-information-n4",
        AuditInstance.from_values(
            ("2/5", "3/10", "1/5", "1/10"),
            ("1/10", "1/5", "4/5", "1"),
            "1/10",
            "1/20",
        ),
        (Fraction(3, 25), Fraction(9, 50), Fraction(7, 10), Fraction(9, 10)),
        Fraction(1, 4),
    ),
    Case(
        "clipped-score-n4",
        AuditInstance.from_values(
            ("2/5", "3/10", "1/5", "1/10"),
            ("4/5", "7/10", "1/2", "1/5"),
            "3/20",
            "1/20",
        ),
        (Fraction(9, 10), Fraction(3, 5), Fraction(2, 5), Fraction(3, 20)),
        Fraction(1, 2),
    ),
)


def main() -> None:
    config = ApproxKellyConfig(grid_size=21, payoff_information="oracle")
    action_denominator = 6
    records = []
    for case in CASES:
        instance = case.instance
        box = multiplicative_score_box(
            instance.weights, case.scores, case.relative_error, instance.epsilon
        )
        policies = (
            OracleContributionPolicy(),
            ProportionalValuePolicy(),
            ProportionalMonetaryScorePolicy(case.scores),
            MeshPriorityPolicy(
                box.uncertainty_contributions,
                denominator=action_denominator,
                name="mesh-certified-uncertainty",
            ),
        )
        values = {
            policy.name: evaluate_policy(instance, policy, config) for policy in policies
        }
        mesh = solve_action_mesh(instance, action_denominator, config)
        values["mesh-Bellman"] = mesh.expected_length
        best_comparator = min(
            value for name, value in values.items() if name != "mesh-Bellman"
        )
        records.append(
            {
                "name": case.name,
                "N": instance.size,
                "pi": [fraction_text(value) for value in instance.weights],
                "f": [fraction_text(value) for value in instance.misstatements],
                "scores": [fraction_text(value) for value in case.scores],
                "relative_error": fraction_text(case.relative_error),
                "epsilon": fraction_text(instance.epsilon),
                "delta": fraction_text(instance.delta),
                "certified_uncertainty_priority": [
                    fraction_text(value) for value in box.uncertainty_contributions
                ],
                "expected_tau": {
                    name: {
                        "exact": fraction_text(value),
                        "decimal": decimal_text(value),
                    }
                    for name, value in values.items()
                },
                "mesh_initial_action": [
                    [index + 1, fraction_text(probability)]
                    for index, probability in mesh.initial_action
                ],
                "mesh_states_evaluated": mesh.states_evaluated,
                "mesh_reduction_from_best_comparator": fraction_text(
                    best_comparator - mesh.expected_length
                ),
            }
        )
    output = {
        "schema_version": 1,
        "scope": (
            "Exact for the 21-point candidate grid and strict-full-support action mesh; "
            "payoff ranges use fixed-f oracle information for every policy so the table "
            "isolates sampling and continuation effects."
        ),
        "action_denominator": action_denominator,
        "grid_size": config.grid_size,
        "cases": records,
    }
    path = Path("benchmarks/small-exact.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(path)


if __name__ == "__main__":
    main()
