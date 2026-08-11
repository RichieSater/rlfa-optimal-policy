"""Certificates for bounded-betting, review-cost, and robust-score theorems."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from .counterexample import decimal_text, fraction_text
from .logical import (
    bounded_cost_ratio_supremum,
    expected_cost_until_index,
    fixed_risk_oracle_gap_family,
)
from .robust import (
    BoxAuditProblem,
    expected_time_proportional_to,
    solve_box_costs,
    solve_box_unit_cost,
)
from .separation import calibration_separation_family

ROBUST_EXAMPLE = BoxAuditProblem.from_values(
    weights=("2/5", "1/4", "3/20", "1/10", "3/50", "1/25"),
    lower=("1/10", "1/5", "0", "2/5", "1/4", "0"),
    upper=("9/10", "3/5", "4/5", "4/5", "3/4", "1/2"),
    epsilon="1/10",
)
ROBUST_COSTS = tuple(Fraction(value) for value in (9, 4, 5, 2, 3, 1))


def _fraction_list(values: tuple[Fraction, ...]) -> list[str]:
    return [fraction_text(value) for value in values]


def build_industry_certificate(
    size: int = 100,
    rho: Fraction = Fraction(1, 1000),
    cost_heterogeneity: Fraction = Fraction(100),
) -> dict[str, Any]:
    """Build exact certificates without simulation or floating-point decisions."""

    family = fixed_risk_oracle_gap_family(size, rho)
    instance = family.instance
    lower_witness, upper_witness = family.witness_candidates
    grid_denominator = family.witness_grid_size - 1

    robust = ROBUST_EXAMPLE
    robust_solution = solve_box_unit_cost(robust)
    randomized_expectation = expected_time_proportional_to(
        robust, robust.uncertainty_contributions
    )
    cost_solution = solve_box_costs(robust, ROBUST_COSTS)
    kappa = Fraction(cost_heterogeneity)
    separation = calibration_separation_family(
        size=size,
        contribution_ratio=rho,
        risk_limit=instance.delta,
        bet_cap=Fraction(5, 2),
        epsilon=instance.epsilon,
        cost_heterogeneity=kappa,
    )
    oracle_rates = tuple(instance.contribution(index) for index in range(size))
    effort_costs = (Fraction(1),) + (kappa,) * (size - 1)
    oracle_expected_cost = expected_cost_until_index(oracle_rates, effort_costs, 0)
    sharp_cost_supremum = bounded_cost_ratio_supremum(size, kappa)

    if not family.candidate_wealth_bound < 1 / instance.delta:
        raise AssertionError("witness wealth bound must stay below the rejection threshold")
    if not family.oracle_expected_length > family.prop_m_rank_upper_bound:
        raise AssertionError("the certified oracle comparison must be strict")
    if not randomized_expectation >= robust_solution.cover_number:
        raise AssertionError("randomization cannot beat the box lower bound")
    if separation.prop_ms_expected_reviews != family.oracle_expected_length:
        raise AssertionError("S=f must make prop-MS coincide with the oracle")
    if separation.prop_ms_expected_cost != oracle_expected_cost:
        raise AssertionError("calibration and oracle effort certificates must coincide")
    if not oracle_expected_cost < sharp_cost_supremum:
        raise AssertionError("finite-rho effort must lie below the sharp supremum")

    return {
        "schema_version": 2,
        "arithmetic": "fractions.Fraction exact rational arithmetic",
        "sharp_oracle_lower_bound": {
            "claim": (
                "At delta=1/20, the repeated Proposition-2 oracle has worst-case "
                "approximation-ratio supremum N for expected stopping time."
            ),
            "instance": {
                "N": size,
                "pi": _fraction_list(instance.weights),
                "f": _fraction_list(instance.misstatements),
                "epsilon": fraction_text(instance.epsilon),
                "delta": fraction_text(instance.delta),
                "pi_times_f": [
                    fraction_text(instance.contribution(index))
                    for index in range(instance.size)
                ],
            },
            "released_construction": {
                "betting_rule": "ApproxKelly",
                "lambda_max": "5/2",
                "grid_size": family.witness_grid_size,
                "logical_intersection": True,
                "running_intersection": True,
            },
            "bounded_betting_generalization": {
                "claim": (
                    "For every delta in (0,1), every finite uniform bet cap L, "
                    "and every bounded predictable valid non-control-variate RLFA "
                    "betting strategy, a sufficiently small rational epsilon gives "
                    "the same sharp factor-N stopping-time lower bound."
                ),
                "conditions": [
                    "0 < epsilon < 1/3",
                    "(1 + 2*L*epsilon)^N < 1/delta",
                    "abs(lambda_t(m)) <= L uniformly",
                ],
                "uses_zero_initialization": False,
                "uses_candidate_grid": False,
                "covers_unbounded_bets": False,
                "covers_control_variates": False,
                "instantiated_bet_cap": "5/2",
                "instantiated_wealth_bound": fraction_text(
                    family.candidate_wealth_bound
                ),
            },
            "surviving_grid_witnesses": {
                "candidates": _fraction_list(family.witness_candidates),
                "grid_indices_zero_based": [
                    int(lower_witness * grid_denominator),
                    int(upper_witness * grid_denominator),
                ],
                "separation": fraction_text(family.witness_separation),
                "separation_over_epsilon": fraction_text(
                    family.witness_separation / instance.epsilon
                ),
                "uniform_wealth_upper_bound": fraction_text(
                    family.candidate_wealth_bound
                ),
                "rejection_threshold": fraction_text(1 / instance.delta),
                "wealth_bound_below_threshold": (
                    family.candidate_wealth_bound < 1 / instance.delta
                ),
            },
            "expected_lengths": {
                "literal_simplex_optimum": "1",
                "oracle": fraction_text(family.oracle_expected_length),
                "oracle_decimal": decimal_text(family.oracle_expected_length),
                "prop_M_upper_bound_via_large_item_rank": fraction_text(
                    family.prop_m_rank_upper_bound
                ),
                "prop_M_upper_bound_decimal": decimal_text(
                    family.prop_m_rank_upper_bound
                ),
            },
            "sharpness": {
                "formula": "E_oracle = 1 + (N-1)/(1+rho)",
                "rho": fraction_text(rho),
                "universal_ratio_upper_bound": size,
                "limit_as_rho_decreases_to_zero": size,
                "oracle_is_full_support": True,
                "perfect_scores_prop_MS_equals_oracle": True,
            },
        },
        "sharp_review_cost_lower_bound": {
            "claim": (
                "If max_i(c_i)/min_i(c_i) <= kappa, the sharp worst-case "
                "oracle-to-optimal expected review-cost ratio supremum is "
                "1+(N-1)*kappa; without such a bound it is infinite already at N=2."
            ),
            "cost_model": {
                "large_item_cost": "1",
                "each_small_item_cost": fraction_text(kappa),
                "cost_heterogeneity_kappa": fraction_text(kappa),
            },
            "expected_costs": {
                "literal_simplex_optimum": "1",
                "oracle": fraction_text(oracle_expected_cost),
                "oracle_decimal": decimal_text(oracle_expected_cost),
            },
            "formula_at_finite_rho": "1 + (N-1)*kappa/(1+rho)",
            "sharp_ratio_supremum": fraction_text(sharp_cost_supremum),
            "unbounded_cost_template_N2": "1 + kappa/(1+rho), which diverges as kappa grows",
        },
        "calibration_separation": {
            "claim": (
                "On the same population, point scores equal the realized taints, "
                "yet prop-MS approaches the worst review and cost ratios while a "
                "valid simultaneous interval certificate identifies a one-item optimum."
            ),
            "point_scores_equal_realized_taints": True,
            "interval_design": {
                "large": [
                    fraction_text(separation.certified_box.lower[0]),
                    fraction_text(separation.certified_box.upper[0]),
                ],
                "each_small": ["0", "1"],
                "large_dollar_uncertainty": fraction_text(
                    separation.certified_box.uncertainty_contributions[0]
                ),
                "total_small_dollar_uncertainty": fraction_text(
                    sum(
                        separation.certified_box.uncertainty_contributions[1:],
                        Fraction(0),
                    )
                ),
                "all_realized_taints_contained": True,
            },
            "certified_optimum": {
                "reviews": 1,
                "selected_1_based": [
                    index + 1 for index in separation.certified_cost_solution.selected
                ],
                "cost": fraction_text(separation.certified_cost_solution.total_cost),
            },
            "prop_MS": {
                "expected_reviews": fraction_text(
                    separation.prop_ms_expected_reviews
                ),
                "expected_cost": fraction_text(separation.prop_ms_expected_cost),
            },
        },
        "certified_score_minimax": {
            "claim": (
                "Descending pi_i*(u_i-l_i) is pathwise minimax-optimal for the "
                "simultaneous box certificate under unit review costs."
            ),
            "instance": {
                "N": robust.size,
                "pi": _fraction_list(robust.weights),
                "lower": _fraction_list(robust.lower),
                "upper": _fraction_list(robust.upper),
                "epsilon": fraction_text(robust.epsilon),
                "uncertainty_contributions": _fraction_list(
                    robust.uncertainty_contributions
                ),
                "initial_width": fraction_text(robust.initial_width),
            },
            "unit_cost_solution": {
                "order_1_based": [index + 1 for index in robust_solution.order],
                "optimal_prefix_1_based": [
                    index + 1 for index in robust_solution.optimal_prefix
                ],
                "minimum_reviews": robust_solution.cover_number,
                "residual_widths": _fraction_list(robust_solution.residual_widths),
                "expected_reviews_if_randomized_proportional_to_uncertainty": (
                    fraction_text(randomized_expectation)
                ),
            },
            "heterogeneous_cost_solution": {
                "costs": _fraction_list(ROBUST_COSTS),
                "selected_1_based": [index + 1 for index in cost_solution.selected],
                "total_cost": fraction_text(cost_solution.total_cost),
                "removed_width": fraction_text(cost_solution.removed_width),
                "residual_width": fraction_text(cost_solution.residual_width),
            },
        },
    }


def industry_certificate_json() -> str:
    return json.dumps(build_industry_certificate(), indent=2, sort_keys=True) + "\n"


def write_industry_certificate(path: str | Path) -> None:
    Path(path).write_text(industry_certificate_json(), encoding="utf-8")
