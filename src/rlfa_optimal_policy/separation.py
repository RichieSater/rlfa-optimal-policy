"""Exact separation between point-score sampling and certified uncertainty."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .logical import (
    BoundedBettingOracleGapFamily,
    bounded_betting_oracle_gap_family,
    expected_cost_until_index,
)
from .model import RationalInput, as_fraction
from .robust import BoxAuditProblem, CostOptimalBoxSolution, solve_box_costs


@dataclass(frozen=True)
class CalibrationSeparationFamily:
    """One population where point scores and certified intervals diverge sharply."""

    oracle_family: BoundedBettingOracleGapFamily
    point_scores: tuple[Fraction, ...]
    certified_box: BoxAuditProblem
    review_costs: tuple[Fraction, ...]
    certified_cost_solution: CostOptimalBoxSolution
    prop_ms_expected_reviews: Fraction
    prop_ms_expected_cost: Fraction


def calibration_separation_family(
    size: int,
    contribution_ratio: RationalInput,
    risk_limit: RationalInput,
    bet_cap: RationalInput,
    epsilon: RationalInput,
    cost_heterogeneity: RationalInput = 1,
) -> CalibrationSeparationFamily:
    """Give scores equal to realized taints but intervals favoring the large item.

    The point scores are exactly ``S=f`` and hence prop-MS uses the same rates
    as the contribution oracle.  The simultaneous intervals contain those
    realized taints, but their dollar uncertainty is ``2*epsilon`` on the
    large transaction and totals only ``epsilon/2`` over all small
    transactions.  The certified plan must review the large transaction and
    stops as soon as it does; descending uncertainty therefore stops in one.
    """

    kappa = as_fraction(cost_heterogeneity)
    if kappa < 1:
        raise ValueError("cost_heterogeneity must be at least one")
    family = bounded_betting_oracle_gap_family(
        size=size,
        contribution_ratio=contribution_ratio,
        risk_limit=risk_limit,
        bet_cap=bet_cap,
        epsilon=epsilon,
    )
    instance = family.instance
    upper_large = 2 * instance.epsilon / instance.weights[0]
    lower = (Fraction(0),) * size
    upper = (upper_large,) + (Fraction(1),) * (size - 1)
    box = BoxAuditProblem(instance.weights, lower, upper, instance.epsilon)
    costs = (Fraction(1),) + (kappa,) * (size - 1)
    cost_solution = solve_box_costs(box, costs)
    point_rates = tuple(
        weight * score
        for weight, score in zip(instance.weights, instance.misstatements, strict=True)
    )

    if not all(
        lo <= value <= hi
        for lo, value, hi in zip(lower, instance.misstatements, upper, strict=True)
    ):
        raise AssertionError("constructed intervals must contain the realized taints")
    if box.uncertainty_contributions[0] != 2 * instance.epsilon:
        raise AssertionError("large-item certified uncertainty was constructed incorrectly")
    if sum(box.uncertainty_contributions[1:], Fraction(0)) != instance.epsilon / 2:
        raise AssertionError("small-item certified uncertainty was constructed incorrectly")
    if cost_solution.selected != (0,) or cost_solution.total_cost != 1:
        raise AssertionError("the certified cost optimum must audit only the large item")

    return CalibrationSeparationFamily(
        oracle_family=family,
        point_scores=instance.misstatements,
        certified_box=box,
        review_costs=costs,
        certified_cost_solution=cost_solution,
        prop_ms_expected_reviews=family.oracle_expected_length,
        prop_ms_expected_cost=expected_cost_until_index(point_rates, costs, 0),
    )
