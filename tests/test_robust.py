from fractions import Fraction
from itertools import combinations, permutations, product
from random import Random

import pytest

from rlfa_optimal_policy.robust import (
    BoxAuditProblem,
    expected_time_proportional_to,
    multiplicative_score_box,
    solve_box_costs,
    solve_box_unit_cost,
    stopping_time_for_order,
)


def test_box_interval_and_exact_solution() -> None:
    problem = BoxAuditProblem.from_values(
        weights=("1/2", "1/3", "1/6"),
        lower=("1/5", "0", "1/2"),
        upper=("4/5", "3/4", "1"),
        epsilon="1/8",
    )
    assert problem.uncertainty_contributions == (
        Fraction(3, 10),
        Fraction(1, 4),
        Fraction(1, 12),
    )
    solution = solve_box_unit_cost(problem)
    assert solution.order == (0, 1, 2)
    assert solution.cover_number == 2
    interval = problem.certificate_interval((0, 1), {0: "2/5", 1: "1/2"})
    assert interval.lower == Fraction(9, 20)
    assert interval.upper == Fraction(8, 15)
    assert interval.diameter == Fraction(1, 12)


def test_adaptivity_cannot_beat_sorted_uncertainty_grid() -> None:
    # Exhaustively compare every ordering for many exact small box problems.
    endpoints = (Fraction(0), Fraction(1, 2), Fraction(1))
    weights = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
    endpoint_pairs = tuple((lo, hi) for lo in endpoints for hi in endpoints if lo <= hi)
    for intervals in product(endpoint_pairs, repeat=3):
        lower = tuple(interval[0] for interval in intervals)
        upper = tuple(interval[1] for interval in intervals)
        for epsilon in (Fraction(0), Fraction(1, 12), Fraction(1, 4), Fraction(1, 2)):
            problem = BoxAuditProblem(weights, lower, upper, epsilon)
            solution = solve_box_unit_cost(problem)
            brute_force = min(
                stopping_time_for_order(problem, order)
                for order in permutations(range(problem.size))
            )
            assert solution.cover_number == brute_force


def test_randomized_proportional_policy_is_strictly_suboptimal() -> None:
    problem = BoxAuditProblem.from_values(
        weights=("1/2", "1/3", "1/6"),
        lower=(0, 0, 0),
        upper=(1, 1, 1),
        epsilon="1/2",
    )
    # Auditing item 0 deterministically certifies the target in one audit.
    assert solve_box_unit_cost(problem).cover_number == 1
    assert expected_time_proportional_to(
        problem, problem.uncertainty_contributions
    ) == Fraction(3, 2)


def test_multiplicative_scores_give_prop_ms_priority_without_clipping() -> None:
    problem = multiplicative_score_box(
        weights=("1/2", "1/3", "1/6"),
        scores=("1/5", "3/10", "1/2"),
        relative_error="1/4",
        epsilon="1/20",
    )
    scores = (Fraction(1, 5), Fraction(3, 10), Fraction(1, 2))
    prop_ms_scores = tuple(
        weight * score
        for weight, score in zip(problem.weights, scores, strict=True)
    )
    uncertainty = problem.uncertainty_contributions
    ratios = tuple(d / score for d, score in zip(uncertainty, prop_ms_scores, strict=True))
    assert len(set(ratios)) == 1
    assert solve_box_unit_cost(problem).order == (0, 1, 2)


def test_clipping_changes_the_correct_priority() -> None:
    problem = multiplicative_score_box(
        weights=("1/2", "1/2"),
        scores=("9/10", "3/5"),
        relative_error="1/2",
        epsilon="1/5",
    )
    # pi*S ranks item 0 first, but its upper endpoint clips at one and its
    # certified interval is narrower.  Dollar-weighted uncertainty ranks 1.
    assert problem.weights[0] * Fraction(9, 10) > problem.weights[1] * Fraction(3, 5)
    assert problem.uncertainty_contributions[0] < problem.uncertainty_contributions[1]
    assert solve_box_unit_cost(problem).order[0] == 1


def test_exact_cost_dp_matches_exhaustive_subsets() -> None:
    problem = BoxAuditProblem.from_values(
        weights=("2/5", "3/10", "1/5", "1/10"),
        lower=(0, 0, 0, 0),
        upper=(1, 1, 1, 1),
        epsilon="3/10",
    )
    costs = (Fraction(7), Fraction(3), Fraction(2), Fraction(1))
    solution = solve_box_costs(problem, costs)
    feasible = []
    for size in range(problem.size + 1):
        for selected in combinations(range(problem.size), size):
            residual = problem.initial_width - sum(
                (problem.uncertainty_contributions[index] for index in selected),
                Fraction(0),
            )
            if residual <= problem.epsilon:
                feasible.append((sum((costs[index] for index in selected), Fraction(0)), selected))
    brute_cost = min(feasible)[0]
    assert solution.total_cost == brute_cost == 10
    assert solution.residual_width <= problem.epsilon


def test_exact_cost_dp_exhaustive_random_grid() -> None:
    rng = Random(20260811)
    size = 5
    weights = (Fraction(1, size),) * size
    for _ in range(50):
        widths = tuple(Fraction(rng.randrange(6), 5) for _ in range(size))
        epsilon = Fraction(rng.randrange(5), 10)
        costs = tuple(Fraction(rng.randrange(1, 10)) for _ in range(size))
        problem = BoxAuditProblem(weights, (Fraction(0),) * size, widths, epsilon)
        solution = solve_box_costs(problem, costs)
        brute_cost = min(
            sum((costs[index] for index in selected), Fraction(0))
            for subset_size in range(size + 1)
            for selected in combinations(range(size), subset_size)
            if problem.initial_width
            - sum(
                (problem.uncertainty_contributions[index] for index in selected),
                Fraction(0),
            )
            <= epsilon
        )
        assert solution.total_cost == brute_cost


def test_invalid_box_inputs() -> None:
    with pytest.raises(ValueError):
        BoxAuditProblem.from_values((1,), ("1/2",), ("1/3",), "1/10")
    with pytest.raises(ValueError):
        multiplicative_score_box((1,), ("1/2",), 1, "1/10")


def test_observed_interval_violation_is_never_silently_certified() -> None:
    problem = BoxAuditProblem.from_values((1,), ("1/4",), ("3/4",), "1/10")
    with pytest.raises(ValueError, match="risk claim invalid"):
        problem.certificate_interval((0,), {0: "4/5"})
