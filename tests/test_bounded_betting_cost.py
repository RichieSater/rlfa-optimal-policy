from fractions import Fraction
from functools import cache
from itertools import combinations

import pytest

from rlfa_optimal_policy.logical import (
    bounded_betting_oracle_gap_family,
    bounded_cost_ratio_supremum,
    expected_cost_until_index,
)
from rlfa_optimal_policy.robust import expected_time_proportional_to, solve_box_unit_cost
from rlfa_optimal_policy.separation import calibration_separation_family


def test_bounded_betting_family_uses_only_uniform_cap() -> None:
    family = bounded_betting_oracle_gap_family(
        size=7,
        contribution_ratio="2/7",
        risk_limit="1/100",
        bet_cap=9,
        epsilon="1/10000",
    )
    instance = family.instance
    lower, upper = family.witness_candidates
    assert upper - lower == 2 * instance.epsilon
    assert family.candidate_wealth_bound == (1 + 18 * instance.epsilon) ** 7
    assert family.candidate_wealth_bound < 1 / instance.delta

    # Check the logical part for every possible number of preceding small items.
    for count in range(instance.size):
        history = tuple(range(1, count + 1))
        interval = instance.logical_interval(history)
        assert interval.lower <= lower < upper <= interval.upper

    # Under oracle sampling the payoff is m_star-m at every next-item outcome.
    for witness in family.witness_candidates:
        assert abs(instance.total_misstatement - witness) < 2 * instance.epsilon
    assert family.oracle_expected_length == 1 + Fraction(6, 1 + Fraction(2, 7))


def test_bounded_betting_family_rejects_insufficient_wealth_margin() -> None:
    with pytest.raises(ValueError, match="not small enough"):
        bounded_betting_oracle_gap_family(4, 1, "1/20", "5/2", "1/4")
    with pytest.raises(ValueError, match="bet_cap"):
        bounded_betting_oracle_gap_family(4, 1, "1/20", -1, "1/100")


@pytest.mark.parametrize(
    ("size", "delta", "cap", "epsilon"),
    (
        (2, "9/10", 100, "1/1000000"),
        (10, "1/1000000", 10, "1/1000"),
        (5, "1/2", 0, "1/4"),
    ),
)
def test_bounded_family_spans_risk_limits_and_caps(
    size: int, delta: str, cap: int, epsilon: str
) -> None:
    family = bounded_betting_oracle_gap_family(size, "1/3", delta, cap, epsilon)
    assert family.candidate_wealth_bound < 1 / family.instance.delta
    assert family.witness_separation == 2 * family.instance.epsilon


def test_expected_cost_until_terminal_matches_subset_recursion() -> None:
    rates = (Fraction(2), Fraction(3), Fraction(5), Fraction(7))
    costs = (Fraction(11), Fraction(13), Fraction(17), Fraction(19))
    terminal = 2

    @cache
    def recurse(remaining: frozenset[int]) -> Fraction:
        denominator = sum((rates[index] for index in remaining), Fraction(0))
        answer = Fraction(0)
        for index in remaining:
            probability = rates[index] / denominator
            if index == terminal:
                answer += probability * costs[index]
            else:
                answer += probability * (costs[index] + recurse(remaining - {index}))
        return answer

    assert expected_cost_until_index(rates, costs, terminal) == recurse(
        frozenset(range(len(rates)))
    )


def test_sharp_bounded_cost_formula_and_unbounded_n2_template() -> None:
    size = 8
    rho = Fraction(1, 1000)
    kappa = Fraction(13)
    family = bounded_betting_oracle_gap_family(
        size, rho, "1/20", "5/2", Fraction(1, 20 * size)
    )
    rates = tuple(family.instance.contribution(index) for index in range(size))
    costs = (Fraction(1),) + (kappa,) * (size - 1)
    expected = expected_cost_until_index(rates, costs, 0)
    assert expected == 1 + Fraction(size - 1) * kappa / (1 + rho)
    assert expected < bounded_cost_ratio_supremum(size, kappa)
    assert bounded_cost_ratio_supremum(size, 1) == size

    # With N=2 and fixed rho=1, 1+kappa/2 has no finite kappa-independent bound.
    assert bounded_cost_ratio_supremum(2, 10**6) == 1_000_001


def test_calibration_separates_equal_realized_scores_from_uncertainty() -> None:
    family = calibration_separation_family(
        size=6,
        contribution_ratio="1/100",
        risk_limit="1/20",
        bet_cap="5/2",
        epsilon="1/120",
        cost_heterogeneity=17,
    )
    instance = family.oracle_family.instance
    box = family.certified_box
    d = box.uncertainty_contributions
    assert family.point_scores == instance.misstatements
    assert d[0] == 2 * instance.epsilon
    assert sum(d[1:], Fraction(0)) == instance.epsilon / 2
    assert solve_box_unit_cost(box).cover_number == 1
    assert family.certified_cost_solution.selected == (0,)
    assert family.certified_cost_solution.total_cost == 1

    # No set omitting the large item can stop; every set containing it can.
    small = tuple(range(1, instance.size))
    for count in range(len(small) + 1):
        for audited_small in combinations(small, count):
            assert not box.stops(audited_small)
            assert box.stops((0,) + audited_small)

    point_rates = tuple(
        weight * score
        for weight, score in zip(instance.weights, family.point_scores, strict=True)
    )
    assert expected_time_proportional_to(box, point_rates) == family.prop_ms_expected_reviews
    assert family.prop_ms_expected_reviews == 1 + Fraction(5, 1 + Fraction(1, 100))
    assert family.prop_ms_expected_cost == 1 + Fraction(5 * 17, 1 + Fraction(1, 100))
