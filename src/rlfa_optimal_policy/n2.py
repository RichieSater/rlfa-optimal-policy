"""Exact global characterization for the pinned construction when ``N = 2``."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction

from .confidence import first_round_combined_interval
from .model import AuditInstance
from .policies import OracleContributionPolicy, validate_distribution


def _require_n2(instance: AuditInstance) -> None:
    if instance.size != 2:
        raise ValueError("the exact characterization in this module requires N = 2")


def stopping_items(instance: AuditInstance) -> tuple[int, ...]:
    """Items whose selection makes the audit stop after the first draw."""

    _require_n2(instance)
    return tuple(
        index
        for index in range(2)
        if first_round_combined_interval(instance, index).diameter <= instance.epsilon
    )


def expected_length_from_first_distribution(
    instance: AuditInstance, distribution: Mapping[int, Fraction]
) -> Fraction:
    """Evaluate any literal-simplex first action exactly."""

    _require_n2(instance)
    validate_distribution(instance, (), distribution, "simplex")
    stop_probability = sum(
        (distribution[index] for index in stopping_items(instance)), Fraction(0)
    )
    return 2 - stop_probability


@dataclass(frozen=True)
class N2Characterization:
    """Optimal value and attainment under the relevant support conventions."""

    stopping_items: tuple[int, ...]
    nonstopping_items: tuple[int, ...]
    optimal_value: Fraction
    unrestricted_attained: bool
    full_support_infimum: Fraction
    full_support_attained: bool
    importance_support_infimum: Fraction
    importance_support_attained: bool
    oracle_defined: bool
    oracle_expected_length: Fraction | None
    oracle_is_globally_optimal: bool | None


def characterize_n2(instance: AuditInstance) -> N2Characterization:
    """Return the complete first-stage solution for the pinned N=2 problem."""

    _require_n2(instance)
    stops = stopping_items(instance)
    nonstops = tuple(index for index in range(2) if index not in stops)
    if stops:
        optimal_value = Fraction(1)
    else:
        optimal_value = Fraction(2)

    # The literal simplex is compact and always contains a minimizing action.
    unrestricted_attained = True

    # Strictly positive distributions can approach every boundary action. They
    # attain the optimum unless exactly one item stops at time one.
    full_support_attained = len(stops) != 1

    # Requiring support only on positive fixed contributions permits an optimal
    # boundary action exactly when every nonstopping contribution is zero.
    importance_support_attained = len(stops) != 1 or all(
        instance.contribution(index) == 0 for index in nonstops
    )

    total_contribution = instance.total_misstatement
    if total_contribution == 0:
        oracle_defined = False
        oracle_expected = None
        oracle_optimal = None
    else:
        oracle_defined = True
        oracle_distribution = OracleContributionPolicy().probabilities(instance, ())
        oracle_expected = expected_length_from_first_distribution(
            instance, oracle_distribution
        )
        oracle_optimal = oracle_expected == optimal_value

    return N2Characterization(
        stopping_items=stops,
        nonstopping_items=nonstops,
        optimal_value=optimal_value,
        unrestricted_attained=unrestricted_attained,
        full_support_infimum=optimal_value,
        full_support_attained=full_support_attained,
        importance_support_infimum=optimal_value,
        importance_support_attained=importance_support_attained,
        oracle_defined=oracle_defined,
        oracle_expected_length=oracle_expected,
        oracle_is_globally_optimal=oracle_optimal,
    )
